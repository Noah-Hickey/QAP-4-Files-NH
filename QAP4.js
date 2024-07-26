//Testing an alert.
alert("Welcome to the Birch Corner Motel customer information!");

//Room Rates
const roomRate = 68.00 //Per night
const delroomRate = 101.00 //Per night

//Customer Information.
console.log("Customer Information");
let custFirstname = "Noah";
let custLastname = "Hickey";
let birthDate = new Date("October 31, 1998");
let gender = "Male";
let roomPref = ["Non-smoking", "Deluxe Room", "Daily Cleaning"];
let paymentMethod = "Credit Card";
let mailingAddress = {
  street: "105 Apple Boulevard",
  city: "St. John's",
  prov: "NL",
  zip: "AAB 567"
};
let phoneNum = "555-1098";
let checkInDate = new Date ("2024-08-01");
let checkOutDate = new Date ("2024-08-03");

//Determines duration of stay
function getdurationStay(checkInDate, checkOutDate) {
  const timeDiff = Math.abs(checkOutDate.getTime() - checkInDate.getTime());
  const diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
  return diffDays;
}


//Deterines age
function getAge(birthDate) {
  const today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDifference = today.getMonth() - birthDate.getMonth();
  if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
}

// Calculate total room rate
function calculateRoomRate(roomPref, duration) {
  let rate = roomPref.includes("Deluxe Room") ? delroomRate : roomRate;
  return rate * duration;
}



//Function to generate a description.
function generateDescription() {
  let duration = getdurationStay(checkInDate, checkOutDate);
  let totalRate = calculateRoomRate(roomPref, duration);
  return `
    <p>Customer Name: ${custFirstname} ${custLastname}</p>
    <p>Age: ${getAge(birthDate)}</p>
    <p>Gender: ${gender}</p>
    <p>Room Preferences: ${roomPref.join(', ')}</p>
    <p>Payment Method: ${paymentMethod}</p>
    <p>Mailing Address: ${mailingAddress.street}, ${mailingAddress.city}, ${mailingAddress.prov} ${mailingAddress.zip}</p>
    <p>Phone Number: ${phoneNum}</p>
    <p>Check-in Date = ${checkInDate.toDateString()}</p>
    <p>Check-out Date: ${checkOutDate.toDateString()}</p>
    <p>Duration of Stay: ${duration} days</p>
    <p>Total Room Rate: $${totalRate.toFixed(2)}</p>
  `;
}


// Display customer information
console.log(generateDescription());

console.log("Have a wonderful stay!");

// Display customer information in the HTML document
document.getElementById("customer-info").innerHTML = generateDescription();
