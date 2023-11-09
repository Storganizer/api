let instance;

class Registry {
  properties = {
    'application': false,
    'eventBus': false,
    'dataStore': false,
    'test': false,
  }

  constructor() {
    if (instance) {
      throw new Error("New instance cannot be created!!")
    }

    instance = this;
  }



  set test(value) {
    this.properties['test'] = value
  }
  get test() {
    return this.properties['test']
  }


  set application(value) {
    this.properties['application'] = value
  }
  get application() {
    return this.properties['application']
  }

  set dataStore(value) {
    this.properties['dataStore'] = value
  }
  get dataStore() {
    return this.properties['dataStore']
  }

  set eventBus(value) {
    this.properties['eventBus'] = value
  }
  get eventBus() {
    return this.properties['eventBus']
  }


}

let registryInstance = Object.freeze(new Registry())

export default registryInstance