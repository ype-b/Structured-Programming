function loadProductByID_mongo()
{
    sendData =
    {
        productId : document.forms['productsearch'].product_id.value
    }

    fetch('/productfetchmongo',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadPopularProducts() {
    fetch('/popularproducts')
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadPopularProducts_thisWeek() {
    fetch('/popularproducts_thisweek')
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadSimmilarProducts()
{
    sendData =
    {
        productId : document.forms['productsearch'].product_id.value
    }

    fetch('/productsfetchsimilar',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadSimmilarVisitors()
{
    sendData =
    {
        visitorId : document.forms['visitorsearch'].visitor_id.value
    }

    fetch('/visitorfetchsimilar',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadProductsBasedOnBrand()
{
    sendData =
    {
        visitorId : document.forms['visitorsearch'].visitor_id.value
    }

    fetch('/productfetchsimilarbrand',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable(products_json));
}

function loadProductByID_postgres()
{
    sendData =
    {
        productId : document.forms['productsearch'].product_id.value
    }

    fetch('/productfetchpostgres',
    {
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body: JSON.stringify(sendData)
    })
        .then(response => response.json())
        .then(products_json => showProductsInTable_postgres(products_json));
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


function showProductsInTable_postgres(products) {
    for (product of products) {
        var row = element("tr",
            element("td", text(product['_id'])),
            element("td", text(product['selling_price']))
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