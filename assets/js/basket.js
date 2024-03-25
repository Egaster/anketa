let cart = {
    'INM-600' : {
        "name" : "INM-600",
        "count" : 3
    }, /*артикул(data-id) : структура с атрибутами*/
    'num2' : 3, /*товар номер 2*/
}




//вывод

document.onclick = event => {
    if (event.target.classList.contains('plus') || event.target.classList.contains('fa-basket-shopping'))
    {
        plusFunction(event.target.dataset.id);
    } 
    if (event.target.classList.contains('') || event.target.classList.contains(''))
    {
        plusFunction(event.target.dataset.id);
    } 
    
    
}


//увеличение кол-ва товара
const plusFunction = id => {
    cart[id]['count'] ++;
    renderCart();
}

//уменьшение кол-ва товара
const minusFunction = id => {
    if(card[id]['count']-1 == 0)
    {
        deleteFunction(id);
        return true;
    }
    cart[id]['count'] --;
    renderCart();
}

//удаление
const deleteFunction = id => {
    delete cart[id];
    renderCart();
}

const renderCart = () => {
    console.log(cart);
}

renderCart();

