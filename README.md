### Для добавления, удаления, редактирования товара необходимо авторизоваться под учетной записью сотрудника магазина staff.
### Имеются две зарегистрированные учeтные записи с таким статусом: 
 - [ ] admin, (pass:admin);
 - [ ]  staff1, (pass:1234).

Добавить статус **staff** для учетной записи можно в консоли admin

 > ### После авторизации c признаком staff, в разделе Товары, станет доступна кнопка(ссылка)
 +добавить товар
 > ### После авторизации как staf, нажав на карточку товара можно перейти на страницу редактирования удаления карточки товара

Зарегистрированы 2 покупателя с наполненными корзинами.
User1 / 1234; User2 / 1234.

Реализована система скидок. Действующие скидки суммируются.
Условия скидок определяются по различным параметрам пользователем со статусом staff на странице  .discounts-manage/, закладка "Управление скидками".

Каждый товар оформленный со скидкой отмечен знаком - кленовый листок 🍁.

Товары, добавленные в корзину, помечаются специальным знаком - "корзина" 🛒 на карточке товара с учетом покупателя.

Избранные товары помечаются специальным знаком - 💗.

Товары для сравнения отмечаются специальным знаком - 👭.

У товаров с активированными отметками, значки яркого цвета, с не активированными - значки бледного оттенка. 

Фильтр товаров по категории, цене, по признаку избранное - доступен на странице .goods/, Товары.

Сортировка товаров по цене доступна на странице .goods/, Товары.

Сортировка по наименованию, категории, цене доступна на странице .compare-goods/, закладка "Сравнить".
