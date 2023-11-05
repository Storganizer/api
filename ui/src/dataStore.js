
export default {
  locations: false,
  boxes: false,
  items: false,

  getLocationById(id) {
    function filterByID(item) {
      if (Number.isFinite(item.id) && item.id == id) {
        return true
      }
      return false
    }

    return this.locations.filter(filterByID)[0]
  },

  getLocations() {
    if (!this.locations) {
      this.locations = this.fetchLocations()
    }

    return this.locations
  },

  fetchLocations() {
    let target = this
    const locationsPromise = fetch("http://10.1.1.79:5000/locations")
      .then((response) => response.json())
      .then((locations) => {
        return locations
      })

    const setLocationInternally = () => {
      locationsPromise.then((locations) => {
        alert(locations)
        target.locations = locations
      })
    }

    setLocationInternally();







/*    this.locations = fetch("http://10.1.1.79:5000/locations")
      .then((response) => response.json())
      .then((locations) => {
        return locations;
      });*/
  },

}