const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        // console.log("Search", searchValue);
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
        fetch("/expenses/search-expenses/", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            // console.log(data);
            appTable.style.display = "none";
            tableOutput.style.display = "block";

            // console.log("data.length", data.length);

            if (data.length === 0) {
                noResults.style.display = "block";
                tableOutput.style.display = "none";
            } else {
                noResults.style.display = "none";
                data.forEach((item) => {
                    const originalDate = new Date(item.date);
                    const options = { year: 'numeric', month: 'long', day: 'numeric' };
                    const formattedDate = originalDate.toLocaleDateString('es-ES', options);
                    tbody.innerHTML += `
                        <tr>
                            <td><i class="mdi mdi-calendar-blank-outline mdi-20px text-danger me-3"></i><span class="fw-medium">${ formattedDate }</span></td>
                            <td>${ item.category__name }</td>
                            <td>${ item.description }</td>
                            <td class="text-end"><span class="badge rounded-pill bg-label-primary me-1">${ item.amount.toFixed(2) }</span></td>
                            <td class="text-center">
                                <div class="dropdown">
                                    <button type="button" class="btn p-0 dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="mdi mdi-dots-vertical"></i></button>
                                    <div class="dropdown-menu">
                                        <a class="dropdown-item" href="/add-expense/edit/${ item.id }/"><i class="mdi mdi-pencil-outline me-1"></i> Editar</a>
                                        <a class="dropdown-item" href="/add-expense/delete/${ item.id }/"><i class="mdi mdi-trash-can-outline me-1"></i> Eliminar</a>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    `;
                });
            }
        });
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});