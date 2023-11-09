import * as riot from 'riot'
import observable from 'riot-observable'
import Registry from './components/application/registry.js'

import Application from './components/application/application.riot'
import DataStore from './components/application/dataStore'

Registry.eventBus = observable()
Registry.dataStore = DataStore

riot.install(function(component) {
  // all components will pass through here
  component.registry = Registry
  return component
})

const mountApp = riot.component(Application)
const app = mountApp(
  document.getElementById('root'),
  {}
)
