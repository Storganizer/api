import * as riot from 'riot'
import Application from './components/application/application.riot'
import DataStore from './components/application/dataStore'

const registry = {
  dataStore: DataStore
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
