import * as riot from 'riot'
import Application from './components/application/application.riot'
import DataStore from './components/application/dataStore'

window.dataStore = DataStore

const mountApp = riot.component(Application)

const app = mountApp(
  document.getElementById('root'),
  {}
)

window.application = app
