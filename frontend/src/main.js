import 'primeicons/primeicons.css';
import 'primeflex/primeflex.min.css';
import './assets/app.css';
import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import Lara from '@primeuix/themes/lara';
import Button from 'primevue/button';
import Select from 'primevue/select';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';

const app = createApp(App);
app.use(PrimeVue, {
  theme: {
    preset: Lara,
    options: {
      darkModeSelector: '.my-app-dark'
    }
  }
});
app.use(ToastService);
app.component('Toast', Toast);
app.component('Button', Button);
app.component('Select', Select);
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('IconField', IconField);
app.component('InputIcon', InputIcon);
app.component('InputText', InputText);
app.mount('#app');
