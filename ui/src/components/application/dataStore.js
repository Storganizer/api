import Registry from './registry.js'



let apiHost = "http://localhost:5000"

export default {

  locations: {
    locations: false,

    search(string) {
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
        return false
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

    search(string) {
      if (!this.boxes) {
        this.fetchBoxes()
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

      return this.boxes.filter(filterByString)
    },

    getBoxById(id) {
      if (!this.boxes) {
        this.fetchBoxes()
        return false
      }

      function filterByID(item) {
        if (Number.isFinite(item.id) && item.id == id) {
          return true
        }
        return false
      }

      return this.boxes.filter(filterByID)[0]
    },

    getBoxesByLocationId(locationId) {
      if (!this.boxes) {
        this.fetchBoxes()
        return []
      }

      function filterByLocationID(item) {
        if (Number.isFinite(item.locationId) && item.locationId == locationId) {
          return true
        }
        return false
      }

      return this.boxes.filter(filterByLocationID)
    },

    getBoxes() {
      if (!this.boxes) {
        this.fetchBoxes()
        return []
      }

      return this.boxes
      return true
    },

    fetchBoxes() {
      if (this.boxes == false) {
        let target = this
        function reqListener() {
          let jsonResponse = JSON.parse(this.responseText)
          target.boxes = jsonResponse
          Registry.eventBus.trigger('dataBoxLoadSuccess', target.boxes)
        }

        const req = new XMLHttpRequest();
        req.addEventListener("load", reqListener);
        req.open("GET", apiHost + "/boxes");
        req.send();
      }
    },

    reload() {
      this.boxes = false
      this.fetchBoxes()
    },

    updateEntry(box) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("PUT", apiHost + "/box/" + box.id)
      req.send(JSON.stringify(box))
    },

    addEntry(box) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("POST", apiHost + "/boxes")
      req.send(JSON.stringify(box))
    },

    deleteEntry(box) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("DELETE", apiHost + "/box/" + box.id)
      req.send()
    }


  },


  items: {
    items: false,

    search(string) {
      if (!this.items) {
        this.fetchItems()
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

      return this.items.filter(filterByString)
    },

    getItemById(id) {
      if (!this.items) {
        this.fetchItems()
        return []
      }

      function filterByID(item) {
        if (Number.isFinite(item.id) && item.id == id) {
          return true
        }
        return false
      }

      return this.items.filter(filterByID)[0]
    },

    getItemsByBoxId(boxId) {
      if (!this.items) {
        this.fetchItems()
        return []
      }

      function filterByBoxID(item) {
        if (Number.isFinite(item.boxId) && item.boxId == boxId) {
          return true
        }
        return false
      }

      return this.items.filter(filterByBoxID)
    },

    getItems() {
      if (!this.items) {
        this.fetchItems()
        return []
      }

      return this.items
    },

    fetchItems() {
      if (this.items == false) {
        let target = this
        function reqListener() {
          let jsonResponse = JSON.parse(this.responseText)
          target.items = jsonResponse
          Registry.eventBus.trigger('dataItemLoadSuccess', target.items)
        }

        const req = new XMLHttpRequest();
        req.addEventListener("load", reqListener);
        req.open("GET", apiHost + "/items");
        req.send();
      }

    },


    reload() {
      this.items = false
      this.fetchItems()
    },

    updateEntry(item) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("PUT", apiHost + "/item/" + item.id)
      req.send(JSON.stringify(item))
    },

    addEntry(item) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("POST", apiHost + "/items")
      req.send(JSON.stringify(item))
    },

    deleteEntry(item) {
      let target = this
      function reqListener() {
        let jsonResponse = JSON.parse(this.responseText)
        target.reload()
      }

      const req = new XMLHttpRequest()
      req.addEventListener("load", reqListener)
      req.open("DELETE", apiHost + "/item/" + item.id)
      req.send()
    }



  },

}
