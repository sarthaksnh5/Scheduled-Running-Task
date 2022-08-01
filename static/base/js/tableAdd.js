let count = 0;
let tableContent = document.getElementById("content");
let submitBtn = document.getElementById("submitBtn");
let submitSpinner = document.getElementById("submitSpinner");
submitSpinner.style.visibility = "hidden";
let dangerAlert = document.getElementById("danger-alert");
dangerAlert.style.display = "None";
let entryCount = 0;

function addRow() {
  let row = tableContent.insertRow(count + 1);
  let cell1 = row.insertCell(0);
  cell1.innerHTML = `
        <div class="form-group">            
          <input type="text" id=fileCount_${entryCount} class="form-control" onfocusout="fileCount(this.value)" /> 
        </div>
  `;
  entryCount = entryCount + 1;
  count = count + 1;
}

function fileCount(num) {
  if (num != "") {
    if (isNaN(num)) {
      dangerAlert.innerHTML = "Please Fill Number";
      dangerAlert.style.display = "block";
      return;
    }
    dangerAlert.style.display = "None";
    if (num == 1) {
      insertOneCell(tableContent.rows[count]);
    } else {
      insertRestRow(tableContent.rows[count]);
      for (let i = 0; i < parseInt(num); i++) {
        let row = tableContent.insertRow(count + 1);
        insertFileOrder(row, i);
        count = count + 1;
      }
    }
  }
}

function insertRestRow(row) {
  let cell2 = row.insertCell(1);
  cell2.innerHTML = `
        <div class="form-group">            
            
        </div>
          `;

  let cell3 = row.insertCell(2);
  cell3.innerHTML = `
          <div class="form-group">
            <input
                type="time"
                class="form-control"
                id="startTime_0_${entryCount - 1}"
                name="startTime_0_${entryCount - 1}"
                placeholder="Start Time"
            />             
          </div>
                `;
  let cell4 = row.insertCell(3);
  cell4.innerHTML = `
      <div class="form-group">        
        <input
            type="time"
            class="form-control"
            id="endTime_0_${entryCount - 1}"
            name="endTime_0_${entryCount - 1}"
            placeholder="End Time"
        />
      </div>
  `;
  let cell5 = row.insertCell(4);
  cell5.innerHTML = `
      <div class="form-group">        
        <select class='form-control' name='looping_0_${
          entryCount - 1
        }' id='looping_0_${entryCount - 1}'>
          <option value='0'>No</option>
          <option value='1'>Yes</option>
        </select>
      </div>
  `;
}

function insertFileOrder(row, i) {
  let cell1 = row.insertCell(0);
  cell1.innerHTML = `
        <div class="form-group">            
            
        </div>
          `;

  let cell2 = row.insertCell(1);
  cell2.innerHTML = `
        <div class="form-group">            
            <input
              type="file"
              class="form-control"
              name="file_${i}_${entryCount - 1}"
              id="file_${i}_${entryCount - 1}"
            />
        </div>
          `;

  let cell3 = row.insertCell(2);
  cell3.innerHTML = `
                    <div class="form-group">                        
                    </div>
                        `;
  let cell4 = row.insertCell(3);
  cell4.innerHTML = `
              <div class="form-group">                        
              </div>
          `;
  let cell5 = row.insertCell(4);
  cell5.innerHTML = `
              <div class="form-group">                        
              </div>
          `;

  let cell6 = row.insertCell(5);
  cell6.innerHTML = `
              <div class="form-group">        
                <input
                  type="text"
                  class="form-control"
                  id="time_${i}_${entryCount - 1}"
                  name="time_${i}_${entryCount - 1}"
                  placeholder="Time (in seconds)"
                />
              </div>
          `;
}

function insertOneCell(row) {
  let cell2 = row.insertCell(1);
  cell2.innerHTML = `
        <div class="form-group">            
            <input
              type="file"
              class="form-control"
              name="file_0_${entryCount - 1}"
              id="file_0_${entryCount - 1}"
            />
        </div>
          `;
  let cell3 = row.insertCell(2);
  cell3.innerHTML = `
            <div class="form-group">
              <input
                  type="time"
                  class="form-control"
                  id="startTime_0_${entryCount - 1}"
                  name="startTime_0_${entryCount - 1}"
                  placeholder="Start Time"
              />             
            </div>
                `;
  let cell4 = row.insertCell(3);
  cell4.innerHTML = `
      <div class="form-group">        
        <input
            type="time"
            class="form-control"
            id="endTime_0_${entryCount - 1}"
            name="endTime_0_${entryCount - 1}"
            placeholder="End Time"
        />
      </div>
  `;
  let cell5 = row.insertCell(4);
  cell5.innerHTML = `
      <div class="form-group">        
        <select class='form-control' name='looping_0_${
          entryCount - 1
        }' id='looping_0_${entryCount - 1}'>
          <option value='0'>No</option>
          <option value='1'>Yes</option>
        </select>
      </div>
  `;
}

function deleteRow() {
  if (count > 0) {
    tableContent.deleteRow(count);
    count = count - 1;
  }
}

function submitForm() {
  dangerAlert.style.display = "None";
  submitSpinner.style.visibility = "visible";
  submitBtn.style.visibility = "hidden";
  var fd = new FormData();
  var csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  fd.append("count", entryCount);
  for (let i = 0; i < parseInt(entryCount); i++) {
    var fileCount = document.getElementById(`fileCount_${i}`).value;
    fd.append(`fileCount_${i}`, fileCount);
    if (fileCount != 1) {
      const startTime = document.getElementById(`startTime_0_${i}`);
      const endTime = document.getElementById(`endTime_0_${i}`);
      const looping = document.getElementById(`looping_0_${i}`);
      fd.append(`startTime_0_${i}`, startTime.value);
      fd.append(`endTime_0_${i}`, endTime.value);
      fd.append(`looping_0_${i}`, looping.value);
      for (let j = 0; j < parseInt(fileCount); j++) {
        const file = document.getElementById(`file_${j}_${i}`);
        const order = document.getElementById(`time_${j}_${i}`);
        fd.append(`file_${j}_${i}`, file.files[0]);
        fd.append(`time_${j}_${i}`, order.value);
      }
    } else {
      const startTime = document.getElementById(`startTime_0_${i}`);
      const endTime = document.getElementById(`endTime_0_${i}`);
      const looping = document.getElementById(`looping_0_${i}`);
      const file = document.getElementById(`file_0_${i}`);
      fd.append(`startTime_0_${i}`, startTime.value);
      fd.append(`endTime_0_${i}`, endTime.value);
      fd.append(`looping_0_${i}`, looping.value);
      fd.append(`file_0_${i}`, file.files[0]);
    }
  }

  fd.append("csrfmiddlewaretoken", csrf);
  var request = new XMLHttpRequest();
  request.onload = function () {
    const response = JSON.parse(this.responseText);
    console.log(response.result);
    if (response.result) {
      location.replace("/base");
    } else {
      dangerAlert.innerHTML = response.message;
      dangerAlert.style.display = "block";
    }
    submitSpinner.style.visibility = "hidden";
    submitBtn.style.visibility = "visible";
  };
  request.open("POST", "/add", true);
  request.send(fd);
}
