import './index.css'
import '@riotjs/hot-reload'
import { mount, install } from 'riot'
import registerGlobalComponents from './register-global-components'
import dataStore from './dataStore'

// register
registerGlobalComponents()

// mount all the global components found in this page
mount('[data-riot-component]')

install(function(component) {
  // all components will pass through here
  component.dataStore = dataStore
})