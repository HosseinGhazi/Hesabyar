import sys
import sqlite3
import os
print(os.getcwd())

# اتصال به دیتابیس
connection = sqlite3.connect("hesabyar.db")

cursor = connection.cursor()

# ساخت جدول کالاها
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        quantity INTEGER
    )
""")

connection.commit()

from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView,
    QStackedWidget
)
from PySide6.QtCore import Qt

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("حساب‌یار | نرم افزار حسابداری فروشگاه")
window.resize(1000, 650)


# =========================
# ساختار صفحات برنامه
# =========================

pages = QStackedWidget()


# =========================
# صفحه شروع
# =========================

home_page = QWidget()
home_layout = QVBoxLayout(home_page)

home_layout.addStretch()

home_title = QLabel("🧾 حساب‌یار")
home_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
home_layout.addWidget(home_title)


home_dashboard_btn = QPushButton("🏠  داشبورد")
home_products_btn = QPushButton("📦  کالاها")
home_purchases_btn = QPushButton("🛒  خرید")
home_sales_btn = QPushButton("🛍  فروش")
home_customers_btn = QPushButton("👥  مشتریان")
home_suppliers_btn = QPushButton("🏢  تأمین‌کنندگان")
home_expenses_btn = QPushButton("💰  هزینه‌ها")
home_reports_btn = QPushButton("📊  گزارش‌ها")
home_settings_btn = QPushButton("⚙️  تنظیمات")


home_buttons = [
    home_dashboard_btn,
    home_products_btn,
    home_purchases_btn,
    home_sales_btn,
    home_customers_btn,
    home_suppliers_btn,
    home_expenses_btn,
    home_reports_btn,
    home_settings_btn
]


for button in home_buttons:
    button.setMinimumHeight(45)
    home_layout.addWidget(button)


home_layout.addStretch()

pages.addWidget(home_page)


# =========================
# صفحه ماژول‌ها
# =========================

module_page = QWidget()

module_layout = QHBoxLayout(module_page)


# =========================
# منوی کناری
# =========================

sidebar = QVBoxLayout()

title = QLabel("🧾 حساب‌یار")

dashboard_btn = QPushButton("🏠  داشبورد")
products_btn = QPushButton("📦  کالاها")
purchases_btn = QPushButton("🛒  خرید")
sales_btn = QPushButton("🛍  فروش")
customers_btn = QPushButton("👥  مشتریان")
suppliers_btn = QPushButton("🏢  تأمین‌کنندگان")
expenses_btn = QPushButton("💰  هزینه‌ها")
reports_btn = QPushButton("📊  گزارش‌ها")
settings_btn = QPushButton("⚙️  تنظیمات")


sidebar.addWidget(title)
sidebar.addWidget(dashboard_btn)
sidebar.addWidget(products_btn)
sidebar.addWidget(purchases_btn)
sidebar.addWidget(sales_btn)
sidebar.addWidget(customers_btn)
sidebar.addWidget(suppliers_btn)
sidebar.addWidget(expenses_btn)
sidebar.addWidget(reports_btn)

sidebar.addStretch()

sidebar.addWidget(settings_btn)


# =========================
# محتوای ماژول
# =========================

content = QVBoxLayout()

welcome = QLabel("به نرم افزار حسابداری حساب‌یار خوش آمدید")
content.addWidget(welcome)


module_layout.addLayout(sidebar)
module_layout.addLayout(content)

pages.addWidget(module_page)


# =========================
# قرار دادن صفحات در پنجره
# =========================

main_layout = QVBoxLayout()
main_layout.addWidget(pages)

window.setLayout(main_layout)

# بخش کالاها
form_created = False

def show_products():
    global form_created

    pages.setCurrentWidget(module_page)

    if form_created:
        return

    form_created = True
    editing_product_id = None

    welcome.setText("📦 مدیریت کالاها")

    # ساخت جدول کالاها
    products_table = QTableWidget()
    products_table.setColumnCount(7)
    products_table.setHorizontalHeaderLabels([
        "شناسه", "نام کالا", "قیمت", "موجودی",
        "ارزش موجودی", "ویرایش", "حذف"
    ])

    products_table.setEditTriggers(
        QAbstractItemView.EditTrigger.NoEditTriggers
    )

    content.addWidget(products_table)

    # فیلدهای فرم
    name_input = QLineEdit()
    name_input.setPlaceholderText("نام کالا")

    price_input = QLineEdit()
    price_input.setPlaceholderText("قیمت کالا")

    quantity_input = QLineEdit()
    quantity_input.setPlaceholderText("تعداد موجودی")

    error_label = QLabel("")
    error_label.setStyleSheet("color: red;")

    save_button = QPushButton("ثبت کالا")
    new_item_button = QPushButton("ثبت کالای جدید")
    new_item_button.hide()

    content.addWidget(name_input)
    content.addWidget(price_input)
    content.addWidget(quantity_input)
    content.addWidget(error_label)
    content.addWidget(save_button)
    content.addWidget(new_item_button)

    # پاک کردن فرم
    def clear_form():
        name_input.clear()
        price_input.clear()
        quantity_input.clear()
        error_label.clear()

        name_input.setStyleSheet("")
        price_input.setStyleSheet("")
        quantity_input.setStyleSheet("")

    # آماده‌سازی فرم برای ثبت کالای جدید
    def reset_form():
        nonlocal editing_product_id

        editing_product_id = None
        clear_form()

        welcome.setText("📦 ثبت کالای جدید")

        save_button.setText("ثبت کالا")
        save_button.show()
        new_item_button.hide()

        name_input.setFocus()

    # به‌روزرسانی جدول
    def refresh_table():
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        products_table.setRowCount(0)
        products_table.setRowCount(len(products))

        for row_index, product in enumerate(products):
            product_id, name, price, quantity = product

            values = [
                product_id,
                name,
                price,
                quantity,
                price * quantity
            ]

            for col_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                products_table.setItem(
                    row_index, col_index, item
                )

            # دکمه ویرایش
            edit_button = QPushButton("✏️")
            edit_button.setToolTip("ویرایش کالا")

            edit_button.clicked.connect(
                lambda checked=False, pid=product_id:
                edit_product(pid)
            )

            products_table.setCellWidget(
                row_index, 5, edit_button
            )

            # دکمه حذف
            delete_button = QPushButton("🗑")
            delete_button.setToolTip("حذف کالا")

            delete_button.clicked.connect(
                lambda checked=False, pid=product_id:
                delete_product(pid)
            )

            products_table.setCellWidget(
                row_index, 6, delete_button
            )

    # انتخاب کالا برای ویرایش
    def edit_product(product_id):
        nonlocal editing_product_id

        cursor.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        )
        product = cursor.fetchone()

        if product is None:
            return

        editing_product_id = product_id

        name_input.setText(product[1])
        price_input.setText(str(product[2]))
        quantity_input.setText(str(product[3]))

        name_input.setStyleSheet("")
        price_input.setStyleSheet("")
        quantity_input.setStyleSheet("")
        error_label.clear()

        welcome.setText("✏️ ویرایش کالا")

        new_item_button.hide()
        save_button.setText("ذخیره تغییرات")
        save_button.show()

        name_input.setFocus()
        # حذف کالا
    def delete_product(product_id):
        answer = QMessageBox.question(
            window,
            "حذف کالا",
            "آیا مطمئن هستید که می‌خواهید این کالا را حذف کنید؟",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if answer == QMessageBox.StandardButton.Yes:
            cursor.execute(
                "DELETE FROM products WHERE id = ?",
                (product_id,)
            )
            connection.commit()

            if editing_product_id == product_id:
                reset_form()

            refresh_table()
            welcome.setText("کالا با موفقیت حذف شد ✅")

    # پاک کردن خطای فیلد
    def clear_error(field):
        field.setStyleSheet("")

    name_input.textChanged.connect(
        lambda: clear_error(name_input)
    )
    price_input.textChanged.connect(
        lambda: clear_error(price_input)
    )
    quantity_input.textChanged.connect(
        lambda: clear_error(quantity_input)
    )

    # ثبت کالا یا ذخیره تغییرات
    def save_product():
        nonlocal editing_product_id

        # اگر دکمه مخفی است، عملیات انجام نشود
        if not save_button.isVisible():
            return

        name = name_input.text().strip()
        price_text = price_input.text().strip()
        quantity_text = quantity_input.text().strip()

        name_input.setStyleSheet("")
        price_input.setStyleSheet("")
        quantity_input.setStyleSheet("")
        error_label.clear()

        errors = []

        if not name:
            name_input.setStyleSheet(
                "border: 2px solid red;"
            )
            errors.append("نام کالا را وارد کن.")

        try:
            price = int(price_text)
            if price < 0:
                raise ValueError
        except ValueError:
            price_input.setStyleSheet(
                "border: 2px solid red;"
            )
            errors.append(
                "قیمت باید یک عدد صحیح و غیرمنفی باشد."
            )

        try:
            quantity = int(quantity_text)
            if quantity < 0:
                raise ValueError
        except ValueError:
            quantity_input.setStyleSheet(
                "border: 2px solid red;"
            )
            errors.append(
                "تعداد باید یک عدد صحیح و غیرمنفی باشد."
            )

        if errors:
            error_label.setText("\n".join(errors))
            return

        if editing_product_id is not None:
            cursor.execute(
                """
                UPDATE products
                SET name = ?, price = ?, quantity = ?
                WHERE id = ?
                """,
                (name, price, quantity, editing_product_id)
            )
            connection.commit()

            editing_product_id = None
            welcome.setText(
                "تغییرات با موفقیت ذخیره شد ✅"
            )

        else:
            cursor.execute(
                """
                INSERT INTO products (name, price, quantity)
                VALUES (?, ?, ?)
                """,
                (name, price, quantity)
            )
            connection.commit()

            welcome.setText(
                "کالا با موفقیت ثبت شد ✅"
            )

        refresh_table()

        # پاک کردن فرم پس از ذخیره موفق
        clear_form()

        save_button.setText("ثبت کالا")
        save_button.hide()
        new_item_button.show()

    # حرکت با Enter
    name_input.returnPressed.connect(price_input.setFocus)
    price_input.returnPressed.connect(quantity_input.setFocus)

    quantity_input.returnPressed.connect(
        lambda: save_button.click()
        if save_button.isVisible() else None
    )

    # اتصال دکمه‌ها
    save_button.clicked.connect(save_product)
    new_item_button.clicked.connect(reset_form)

    # نمایش اولیه جدول
    refresh_table()

# اتصال دکمه کالاها
products_btn.clicked.connect(show_products)
home_products_btn.clicked.connect(show_products)


# داشبورد
def show_dashboard():
    pages.setCurrentWidget(module_page)
    welcome.setText("🏠 داشبورد")


dashboard_btn.clicked.connect(show_dashboard)
home_dashboard_btn.clicked.connect(show_dashboard)


# خرید
def show_purchases():
    pages.setCurrentWidget(module_page)
    welcome.setText("🛒 ماژول خرید در حال توسعه است")


purchases_btn.clicked.connect(show_purchases)
home_purchases_btn.clicked.connect(show_purchases)


# فروش
def show_sales():
    pages.setCurrentWidget(module_page)
    welcome.setText("🛍 ماژول فروش در حال توسعه است")


sales_btn.clicked.connect(show_sales)
home_sales_btn.clicked.connect(show_sales)


# مشتریان
def show_customers():
    pages.setCurrentWidget(module_page)
    welcome.setText("👥 ماژول مشتریان در حال توسعه است")


customers_btn.clicked.connect(show_customers)
home_customers_btn.clicked.connect(show_customers)


# تأمین‌کنندگان
def show_suppliers():
    pages.setCurrentWidget(module_page)
    welcome.setText("🏢 ماژول تأمین‌کنندگان در حال توسعه است")


suppliers_btn.clicked.connect(show_suppliers)
home_suppliers_btn.clicked.connect(show_suppliers)


# هزینه‌ها
def show_expenses():
    pages.setCurrentWidget(module_page)
    welcome.setText("💰 ماژول هزینه‌ها در حال توسعه است")


expenses_btn.clicked.connect(show_expenses)
home_expenses_btn.clicked.connect(show_expenses)


# گزارش‌ها
def show_reports():
    pages.setCurrentWidget(module_page)
    welcome.setText("📊 ماژول گزارش‌ها در حال توسعه است")


reports_btn.clicked.connect(show_reports)
home_reports_btn.clicked.connect(show_reports)


# تنظیمات
def show_page():
    pages.setCurrentWidget(module_page)
    welcome.setText("⚙️ تنظیمات در حال توسعه است")


settings_btn.clicked.connect(show_page)
home_settings_btn.clicked.connect(show_page)

purchases_btn.clicked.connect(
    lambda: show_page("🛒 ماژول خرید در حال توسعه است")
)

sales_btn.clicked.connect(
    lambda: show_page("🛍️ ماژول فروش در حال توسعه است")
)

customers_btn.clicked.connect(
    lambda: show_page("👥 ماژول مشتریان در حال توسعه است")
)

suppliers_btn.clicked.connect(
    lambda: show_page("🏢 ماژول تأمین‌کنندگان در حال توسعه است")
)

expenses_btn.clicked.connect(
    lambda: show_page("💰 ماژول هزینه‌ها در حال توسعه است")
)

reports_btn.clicked.connect(
    lambda: show_page("📊 ماژول گزارش‌ها در حال توسعه است")
)

settings_btn.clicked.connect(
    lambda: show_page("⚙️ تنظیمات در حال توسعه است")
)

window.setLayout(main_layout)

window.show()

sys.exit(app.exec())