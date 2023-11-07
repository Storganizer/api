import './index.css'
import '@riotjs/hot-reload'


//import * as riot from 'riot'

import * as riot from 'riot'
import App from './components/application.riot'

const mountApp = riot.component(App)

const app = mountApp(
  document.getElementById('root')
)
















/*import registerGlobalComponents from './register-global-components'
import dataStore from './dataStore'

window.dataStore = dataStore
// register
registerGlobalComponents()

// mount all the global components found in this page
riot.mount('[data-riot-component]')
*/
/*riot.install(function(component) {
  // all components will pass through here
  component.dataStore = dataStore
  return component
})*/
