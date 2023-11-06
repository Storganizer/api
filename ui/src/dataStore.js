
export default {
  locations: false,

  getLocations(callback) {
    console.log('go for it')
    if (!this.locations) {
      this.fetchLocations(callback)
      return false
    }

    callback(this.locations)
    return true
  },

  fetchLocations(callback) {
    if (this.locations == false) {

      function reqListener() {
        callback(JSON.parse(this.responseText))
      }

      const req = new XMLHttpRequest();
      req.addEventListener("load", reqListener);
      req.open("GET", "http://localhost:5000/locations");
      req.send();
    }
  },

}