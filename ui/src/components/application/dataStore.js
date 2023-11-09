import Registry from './registry.js'



let apiHost = "http://localhost:5000"

export default {

  locations: {
    locations: false,

    search(string,) {
      if (!this.locations) {
        this.fetchLocations()
        return []
      }

      string = string.toLowerCase()
      function filterByString(item) {
        if (string == '') {
          return true
        }
        let found = false

        if (item.name && item.name.toLowerCase().includes(string)) {
          found = true
        }

        if (item.description && item.description.toLowerCase().includes(string)) {
          found = true
        }

        return found
      }

      return this.locations.filter(filterByString)
    },

    getLocationById(id) {
      if (!this.locations) {
        this.fetchLocations()
        return []
      }

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
        this.fetchLocations()
        return []
      }

      return this.locations
    },

    fetchLocations() {
      if (this.locations == false) {
        let target = this
        function reqListener() {
          let jsonResponse = JSON.parse(this.responseText)
          target.locations = jsonResponse
          Registry.eventBus.trigger('dataLocationLoadSuccess', target.locations)
        }

        const req = new XMLHttpRequest()
        req.addEventListener("load", reqListener)
        req.open("GET", apiHost + "/locations")
        req.send()

        return false
      } else {
        return true
      }
    },

    reload() {
      this.locations = false
      this.fetchLocations()
    },

    updateEntry(location) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("PUT", apiHost + "/location/" + location.id)
      req.send(JSON.stringify(location))
    },

    addEntry(location) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("POST", apiHost + "/locations")
      req.send(JSON.stringify(location))
    },

    deleteEntry(location) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("DELETE", apiHost + "/location/" + location.id)
      req.send()
    }
  },

  boxes: {
    boxes: false,

    search(string, callback) {
      string = string.toLowerCase()
      function filterByString(item) {
        if (string == '') {
          return true
        }

        let found = false

        if (item.name && item.name.toLowerCase().includes(string)) {
          found = true
        }

        if (item.description && item.description.toLowerCase().includes(string)) {
          found = true
        }

        return found
      }

      if (!this.boxes) {
        this.fetchBoxes(function(data) {
          callback(data.filter(filterByString))
        })
        return false
      }

      callback(this.boxes.filter(filterByString))
      return true
    },

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
        req.open("GET", "http://10.1.1.79:5000/boxes");
        req.send();
      }
    },
  },


  items: {
    items: false,

    search(string, callback) {
      string = string.toLowerCase()
      function filterByString(item) {
        if (string == '') {
          return true
        }

        let found = false

        if (item.name && item.name.toLowerCase().includes(string)) {
          found = true
        }

        if (item.description && item.description.toLowerCase().includes(string)) {
          found = true
        }

        return found
      }

      if (!this.items) {
        this.fetchItems(function(data) {
          callback(data.filter(filterByString))
        })
        return false
      }

      callback(this.items.filter(filterByString))
      return true
    },

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
        req.open("GET", "http://10.1.1.79:5000/items");
        req.send();
      }
    },
  },







}
