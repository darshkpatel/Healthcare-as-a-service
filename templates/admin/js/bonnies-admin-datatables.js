
// Call the dataTables jQuery plugin
$(document).ready(function()
 {

  var socket = io.connect('http://localhost:5000');

  socket.on('orderchange', function (aa) {
      populateTable();
      
  });

  populateTable();
});

console.log("Yash");
var global_row = null;
var API_GLOBAL = "http://localhost:5000/";

function updateOnServer(fulfil)
{
  /*
    fulfil has to be 0 or 1
    orderid is the OrderId from the table
    itemid is the ItemId from the table
  */

  orderid = global_row.getElementsByClassName('order_id')[0].innerHTML;
  itemid = global_row.getElementsByClassName('item_id')[0].innerHTML;

  console.log(orderid);
  console.log(itemid);

  tosend = [orderid, itemid, fulfil];

  global_row = null;
  //return;
  ur = API_GLOBAL + "api/order_update/" + tosend.join("/");

    $.ajax(
      {
        url: ur,
        /*type: 'POST',
        dataType: 'json', // I was pretty sure this would do the trick*/

        success: function (result)
         {
            console.log(result);
        }
      }
    );
    populateTable();

}
var table= null;

function populateTable()
{

    $.ajax({
      url: API_GLOBAL + "api/orders_all", success: function (result) {
        console.log(result);

        if(table!==null)
        {
          table.clear();
          table.destroy();
        }
        /*
        <th>ID</th>
        <th>Item ID</th>
        <th>Item QTY</th>
        <th>Order Date-Time</th>
        <th>Order Time-Fulfilled</th>
        <th>Status</th>
        <th>Name</th>
        <th>Phone Number</th>
        */

        var tbody = $("#tbody");
        tbody.html("");


        result.forEach(element => {
          tr = $(document.createElement('tr'));
          console.log(element['order_id']);

          ['order_id', 'item_id', 'item_quan', 'time_start', 'time_end', 'fulfil', 'name', 'phone_number'].
            forEach(function (attr) 
            {
              td = $(document.createElement("td"));
/*
<a class="nav-link" data-toggle="modal" data-target="#OrderModal"*/
              td.addClass(attr);

              if(attr=="fulfil")
              {
                if (element.fulfil === 1) 
                {
                  tr.addClass("table-success");
                  td.html("Fulfilled");

                }
                else if (element.fulfil === 0) 
                {
                  if (element.time_end != null)
                   {
                    tr.addClass("table-danger");
                    td.html("Cancelled");
                  }
                  else{
                    td.html("In progress..");
                  }
                }
                
              }
              else{
                td.html(element[attr]);

              }
              

              tr.append(td);
            });

          //tr.addEventListener('click', doit, false); //everything else    

          //tr.onclick =
          tbody.append(tr);

        });

        if (table===null) {
          table = $('#dataTable').DataTable();

        }
        else{
          table = $('#dataTable').DataTable({
            responsive: true,
            destroy: true
          });


        }


        /*
        SAMPLE RESPONSE

        */
        $("#dataTable tr").click(function () 
        {
          global_row = this;
          $("#OrderModal").modal('show');


          });

      }
    });
}

/*

*/