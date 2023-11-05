
export default {
  locations: false,

  getLocations() {
    if (!this.locations) {
      this.fetchLocations()
    }

    return this.locations
  },

  async fetchLocations() {
    try {
      const res = await fetch(`http://10.1.1.179:5000/locations`);
      this.locations = await res.json();
    } catch (error) {
      console.log({ error });
    }
  },

  loadLocations() {
    this.locations = [{
      name: 'test',
      description: 'super',
      classification: 1
    }]
    return true
  }
}