from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .models import Menu, Order, OrderItem

from django.contrib.auth.models import User
from django.http import HttpResponse


def menu_page(request):
    items = Menu.objects.filter(is_available=True)
    return render(request, "menu.html", {"items": items})


def confirm_order(request):

    items = Menu.objects.all()
    selected_items = []
    total = 0

    for item in items:
        qty = request.POST.get(f"quantity_{item.id}")

        if qty and int(qty) > 0:
            quantity = int(qty)
            subtotal = quantity * item.price

            selected_items.append({
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

    request.session["order_items"] = selected_items
    request.session["total"] = total

    return render(request, "confirm.html", {
        "items": selected_items,
        "total": total
    })


def place_order(request):

    name = request.POST.get("customer_name")

    order = Order.objects.create(customer_name=name)

    items = request.session.get("order_items", [])

    for item in items:
        menu_item = Menu.objects.get(id=item["id"])

        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=item["quantity"]
        )

    total = request.session.get("total", 0)

    return render(request, "bill.html", {
        "order": order,
        "items": items,
        "total": total
    })


def download_token(request, order_id):

    order = Order.objects.get(pk=order_id)
    items = OrderItem.objects.filter(order=order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="token_{order.token_number}.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, y, "Vincent De Paul Canteen Token")

    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Token Number: {order.token_number}")

    y -= 20
    p.drawString(50, y, f"Customer: {order.customer_name}")

    y -= 20
    p.drawString(50, y, f"Order Time: {order.created_at}")

    y -= 40
    p.drawString(50, y, "Items Ordered:")

    y -= 20

    total = 0

    for item in items:
        subtotal = item.quantity * item.menu_item.price
        total += subtotal

        p.drawString(60, y, f"{item.menu_item.name} x {item.quantity} = ₹{subtotal}")
        y -= 20

    y -= 20
    p.drawString(50, y, f"Total: ₹{total}")

    y -= 40
    p.drawString(50, y, "Please show this token on Sunday to collect your order.")

    p.showPage()
    p.save()

    return response


def dashboard_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")

    return render(request, "login.html")

@login_required
def dashboard(request):

    allowed_users = [
        "developer",
        "Lawrence",
        "CaltonDavid",
        "Priest_judes"
    ]

    if request.user.username not in allowed_users:
        return render(request, "access_denied.html")

    items = Menu.objects.all()

    summary = []
    total_revenue = 0

    for item in items:

        total_qty = OrderItem.objects.filter(menu_item=item).aggregate(
            Sum('quantity')
        )['quantity__sum'] or 0

        revenue = total_qty * item.price
        total_revenue += revenue

        summary.append({
            "name": item.name,
            "total": total_qty,
            "revenue": revenue
        })

    total_orders = Order.objects.count()

    return render(request, "dashboard.html", {
        "summary": summary,
        "total_orders": total_orders,
        "total_revenue": total_revenue
    })

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def kitchen_control(request):

    allowed_users = [
        "developer",
        "Lawrence",
        "CaltonDavid",
        "Priest_judes"
    ]

    if request.user.username not in allowed_users:
        return render(request, "access_denied.html")

    items = Menu.objects.all()

    return render(request, "kitchen_control.html", {"items": items})

@login_required
def toggle_item(request, item_id):

    allowed_users = [
        "developer",
        "vdp_judes_caltondavid",
        "vdp_judes_lawrence",
        "vdp_judespriest"
    ]

    if request.user.username not in allowed_users:
        return render(request, "access_denied.html")

    item = Menu.objects.get(id=item_id)
    item.is_available = not item.is_available
    item.save()

    return redirect("/kitchen-control")

