function loadPopularProducts() {
    fetch('/popularproducts')
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadRecentlyViewedProducts()
{
    fetch('/recentproducts')
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadProductsOOS()
{
    fetch('/productsOOS')
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadProductsSimilar()
{
    sendData =
    {
        productId : document.forms['productsearch'].product_id.value
    }

    fetch('/productsimilar',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadMyProducts()
{
    sendData =
    {
        sessionId : document.forms['invoerformulier'].session_id.value
    }

    fetch('/myproducts',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadProductRecommendations()
{
    sendData =
    {
        loginId : document.forms['userlogin'].login_id.value
    }

    fetch('/productrecommendations',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function showProductsInTable(products) {
    for (product of products) {
        var row = element("tr",
            element("td", text(product['_id'])),
            element("td", text(product['brand'])),
            element("td", text(product['category'])),
            element("td", link(product['deeplink'], product['deeplink']))
        )

        document.querySelector("#products").appendChild(row);
    }
}


function element(name, ...childs) {
    var element = document.createElement(name);
    for (let i=0; i < childs.length; i++) {
        element.appendChild(childs[i]);
    }
    return element;
}

function text(value) {
    return document.createTextNode(value)
}

function link(href, value) {
    var link = document.createElement("a");
    link.appendChild(text(value));
    link.setAttribute("href", href);
    link.setAttribute("target", "blank");
    return link;
}