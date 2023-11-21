// PARA LA MAYORIA DE ELEMENTOS SELECCIONADOS SE USA CONST YA QUE NO SE REASIGNA
const carrito = document.querySelector('#carrito');
const contenedorCarrito = document.querySelector('#lista-carrito tbody');
const vaciarCarritoBtn = document.querySelector('#vaciar-carrito');
const listaCursos = document.querySelector('#lista-cursos');
let articulosCarrito=[];


cargarEventListeners();

function cargarEventListeners(){
    // funcionara cuando aprete agregar al carrito
    listaCursos.addEventListener('click',agregarCurso);

    //elimina cursos del carrito

    carrito.addEventListener('click', eliminarCurso);


    // USO DE LOCAL STORAGE
    document.addEventListener('DOMContentLoaded', () =>{
        articulosCarrito= JSON.parse(localStorage.getItem('carrito')) || [];
        carritoHTML();
    })



    //vaciar carrito se uso funcion anonima , ya que es poco codigo, cuando es arto codigo es recomendable hacr una funcion aparte
    vaciarCarritoBtn.addEventListener('click', () => {
        articulosCarrito=[] // reseteamos el arreglo
        limpiarHTML(); // tambien puede llamarse esta funcion: carritoHTML();.   Elimina tood el htlm
    })

}

//funciones
//es recomendable ir probando paso paso como se va construllendo las funciones con console.log

function agregarCurso(e){ // el e es el evento para identificar a que le dimos click

    e.preventDefault(); // Event Bubbling, se supone en una pagina real al seleccionar añadir al carrito me debiere mandar a otra pagina por eso el HREF
    if(e.target.classList.contains('agregar-carrito')){ // target es hacia donde estamos dando click
        const cursoSeleccionado= e.target.parentElement.parentElement; // va hacia el elemento padre dea ahi su nombre
        leerDatosCurso(cursoSeleccionado);
    }
    
}

//elimina un curso del carrito // el e es el evento para identificar a que le dimos click
function eliminarCurso(e){
    if(e.target.classList.contains('borrar-curso')){
        const cursoId= e.target.getAttribute('data-id');
        // elimina del arreglo de articulosCarrito por el data id
        articulosCarrito=articulosCarrito.filter(curso => curso.id !== cursoId); // me traiga todos los elementos menos el que yo aprete eliminar
        carritoHTML(); // se llama otra vez esta funcion para que muestre nuevamente los elementos del html
    }

}





function leerDatosCurso(curso){
    // console.log(curso);

    // crear un objeto con el conteido del curso actual
    const infocurso={
        imagen: curso.querySelector('img').src,
        titulo: curso.querySelector('h4').textContent, // textContent extrae el texto del h4
        precio: curso.querySelector('.precio span').textContent,
        id: curso.querySelector('a').getAttribute('data-id'), // obtiene el id segun la seleccion del elemento. 
        cantidad: 1
    }

    // revisa si un elemento ya existe en el carrito

    const existe = articulosCarrito.some(curso => curso.id===infocurso.id);// some se usa para objetos. lo que hace esta linea es saber si el id que esta en el arreglo(curso.id) es igual al elemento que se va agregar (infocurso.id))
    if(existe){
        // se actualiza la cantidad
        const cursos = articulosCarrito.map(curso => { // map te crea un nuevo arreglo
            if(curso.id===infocurso.id){
                curso.cantidad++;
                return curso;
            }
            else{
                return curso;
            }
        }) 
        articulosCarrito= [...cursos];
    }
    else{
        //se agrega el curso al carrito
        // agrega elementos al arreglo de carrito
        articulosCarrito=[...articulosCarrito, infocurso]; //...articulosCarrito toma una copia // se agrega articulosCarrito para que guarde el primer elemento que selecciono, para que asi pueda selccionar otro y n pierda el primero

    }

    carritoHTML();
}

// muestra el carrito de compras en el html

function carritoHTML(){
    //limpiar el html
     limpiarHTML(); //comentar para ver lo que pasa en la funcion
    // recorre el carrito y genera el html
    articulosCarrito.forEach(curso => {
        const{imagen,titulo,precio,cantidad, id} = curso
        const row = document.createElement('tr');// Inner Html agrega contenido a una etiqueta especifica en html y el id es necesario porque es la forma de llamar el contenido de html a javascript

        row.innerHTML = `


            <td>
                <img src="${imagen}" width="100">
            </td>

            <td>
                    ${titulo}
            </td>

            <td>
                     ${precio}
            </td>

            <td>
                     ${cantidad}
            </td>

            <td>
                    <a href="#" class="borrar-curso" data-id="${id}"> X </a>
            </td>

            


        `;
        //agrega el html del carrito en el tbody

        contenedorCarrito.appendChild(row); //El appendChild()método agrega un nodo (elemento) como el último hijo de un elemento.


    })
    // NUEVA FUNCION AGREGAR AL STORAGE
    //agrega el carrito de compras al storage
    sincronizarStorage();
}


function sincronizarStorage(){
    localStorage.setItem('carrito', JSON.stringify(articulosCarrito));
}


//elimina los cursos del tbody

function limpiarHTML(){
    //forma lenta
    //contenedorCarrito.innerHTML = ''; // esto se hace para limpiar el html, ya que al agregar un elemento y luego agregar otro elementos se repite el primer elemento , y dejar el iner '' hace que se limpie


    //forma rapida
    while(contenedorCarrito.firstChild){
        contenedorCarrito.removeChild(contenedorCarrito.firstChild) // eliminar desde el padre hacia el hijo, un elemento se elimina por el padre
    }

    /* eso es basicamento lo que hace el while va elimando los hijos
        <div> 
            <p>1</p>
            <p>2</p>
            <p>3</p>
        </div>
    */
}