fetch("http://127.0.0.1:5000/show-products/")
.then(responce => responce.json())
.then(data => {
    console.log(data);
})