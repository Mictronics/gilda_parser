import 'primeicons/primeicons.css';
import 'primeflex/primeflex.min.css';
import './assets/app.css';
import { createApp } from 'vue';
import { definePreset, palette } from '@primeuix/themes';
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
import Dialog from 'primevue/dialog';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';

const Airbus = definePreset(Lara, {
  semantic: {
    primary: {
      0: '#ffffff',
      50: '#f2f4f7',
      100: '#c2c9d8',
      200: '#919fb8',
      300: '#617599',
      400: '#304a7a',
      500: '#00205b',
      600: '#001b4d',
      700: '#001640',
      800: '#001232',
      900: '#000d24',
      950: '#000817'
    },
    colorScheme: {
      light: {
        surface: {
          0: '#ffffff',
          50: '#f2f4f7',
          100: '#c2c9d8',
          200: '#919fb8',
          300: '#617599',
          400: '#304a7a',
          500: '#00205b',
          600: '#001b4d',
          700: '#001640',
          800: '#001232',
          900: '#000d24',
          950: '#000817'
        }
      },
      dark: {
        surface: {
          0: '#ffffff',
          50: '#f2f4f7',
          100: '#c2c9d8',
          200: '#919fb8',
          300: '#617599',
          400: '#304a7a',
          500: '#00205b',
          600: '#001b4d',
          700: '#001640',
          800: '#001232',
          900: '#000d24',
          950: '#000817'
        }
      }
    }
  }
});

const app = createApp(App);
app.use(PrimeVue, {
  theme: {
    preset: Airbus,
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
app.component('Dialog', Dialog);
app.mount('#app');
