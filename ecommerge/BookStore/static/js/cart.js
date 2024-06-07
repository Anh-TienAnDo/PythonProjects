console.log('hello')
var btnAddCart = document.getElementsByClassName('add-cart')
console.log(btnAddCart.length)
for(i=0; i<btnAddCart.length; i++){
    btnAddCart[i].addEventListener('click', function(){
        var product = this.dataset.product
        var action = this.dataset.action
        console.log(product)
        console.log(action)
        console.log(user)
        // AnonymousUser not log in
    })
}