
export default {

  locations: {
    locations: false,

    getLocationById(id, callback) {
      function filterByID(item) {
        if (Number.isFinite(item.id) && item.id == id) {
          return true
        }
        return false
      }

      if (!this.locations) {
        this.fetchLocations(function(data) {
          callback(data.filter(filterByID)[0])
        })
        return false
      }

      callback(this.locations.filter(filterByID)[0])
      return true
    },

    getLocations(callback) {
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
  },

  boxes: {
    boxes: false,

    getBoxById(id, callback) {
      function filterByID(item) {
        if (Number.isFinite(item.id) && item.id == id) {
          return true
        }
        return false
      }

      if (!this.boxes) {
        this.fetchBoxes(function(data) {
          callback(data.filter(filterByID)[0])
        })
        return false
      }

      callback(this.boxes.filter(filterByID)[0])
      return true
    },

    getBoxesByLocationId(locationId, callback) {
      function filterByLocationID(item) {
        if (Number.isFinite(item.locationId) && item.locationId == locationId) {
          return true
        }
        return false
      }

      if (!this.boxes) {
        this.fetchBoxes(function(data) {
          callback(data.filter(filterByLocationID))
        })
        return false
      }

      callback(this.boxes.filter(filterByLocationID))
      return true
    },

    getBoxes(callback) {
      if (!this.boxes) {
        this.fetchBoxes(callback)
        return false
      }

      callback(this.boxes)
      return true
    },

    fetchBoxes(callback) {
      if (this.boxes == false) {
        let target = this
        function reqListener() {
          let jsonResponse = JSON.parse(this.responseText)
          target.boxes = jsonResponse
          callback(jsonResponse)
        }

        const req = new XMLHttpRequest();
        req.addEventListener("load", reqListener);
        req.open("GET", "http://localhost:5000/boxes");
        req.send();
      }
    },
  },


  items: {
    items: false,

    getItemById(id, callback) {
      function filterByID(item) {
        if (Number.isFinite(item.id) && item.id == id) {
          return true
        }
        return false
      }

      if (!this.items) {
        this.fetchItems(function(data) {
          callback(data.filter(filterByID)[0])
        })
        return false
      }

      callback(this.items.filter(filterByID)[0])
      return true
    },

    getItemsByBoxId(boxId, callback) {
      function filterByBoxID(item) {
        if (Number.isFinite(item.boxId) && item.boxId == boxId) {
          return true
        }
        return false
      }

      if (!this.items) {
        this.fetchItems(function(data) {
          callback(data.filter(filterByBoxID))
        })
        return false
      }

      callback(this.items.filter(filterByBoxID))
      return true
    },

    getItems(callback) {
      if (!this.items) {
        this.fetchItems(callback)
        return false
      }

      callback(this.items)
      return true
    },

    fetchItems(callback) {
      if (this.items == false) {
        let target = this
        function reqListener() {
          let jsonResponse = JSON.parse(this.responseText)
          target.items = jsonResponse
          callback(jsonResponse)
        }

        const req = new XMLHttpRequest();
        req.addEventListener("load", reqListener);
        req.open("GET", "http://localhost:5000/items");
        req.send();
      }
    },
  },







}
