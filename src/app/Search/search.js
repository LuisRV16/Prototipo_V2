function initAutocomplete() {
  const input = document.getElementById("autocomplete");
  const autocomplete = new google.maps.places.Autocomplete(input, {
    types: ["geocode"], 
    fields: ["place_id", "geometry", "name"],
  });

  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    console.log("Lugar seleccionado:", place);
  });
}

window.initAutocomplete = initAutocomplete;