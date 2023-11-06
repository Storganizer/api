
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
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.locations = jsonResponse
        callback(jsonResponse)
      }

      const req = new XMLHttpRequest();
      req.addEventListener("load", reqListener);
      req.open("GET", "http://localhost:5000/locations");
      req.send();
    }
  },

}