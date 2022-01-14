//querySelectorAll devuelve una lista de nodos de HTML
//se agrega un 1 a la clase .btn-delete para desactivar la busqueda
const btnDelete = document.querySelectorAll('.btn-delete1');
//revisamos si la lista tiene elementos, esto porque podemos estar en una pagina que no tenga los botones de delete contact
if (btnDelete){
    //Volvemos la lista de nodos HTML en un arreglo para recorrerlos
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('Esta seguro de borrar')){
                e.preventDefault();
            }
        });
    });
}