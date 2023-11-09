import * as riot from 'riot'
import observable from 'riot-observable'
import Application from './components/application/application.riot'
import DataStore from './components/application/dataStore'

const eventBus = observable()
const registry = {
  dataStore: DataStore,
  eventBus: eventBus,
}
riot.install(function(component) {
  // all components will pass through here
  component.registry = registry
  return component
})


window.dataStore = DataStore

const mountApp = riot.component(Application)
const app = mountApp(
  document.getElementById('root'),
  {}
)
