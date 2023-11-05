import './index.css'
import '@riotjs/hot-reload'
import { mount, install } from 'riot'
import registerGlobalComponents from './register-global-components'
import dataStore from './dataStore'

dataStore.getLocations()
window.dataStore = dataStore

// register
registerGlobalComponents()

// mount all the global components found in this page
mount('[data-riot-component]')

window.dataStore = dataStore
