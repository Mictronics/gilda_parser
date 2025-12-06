<template>
  <!DOCTYPE html>
  <title>GILDA Viewer</title>
  <Toast />
  <div class="flex flex-row justify-content-between">
    <div class="flex gap-2">
      <Select
        v-model="selectedDatabase"
        :options="listDatabases"
        optionLabel="name"
        optionValue="path"
        placeholder="Select GILDA database"
        size="small"
      />
      <Button
        label="Load"
        icon="pi pi-database"
        @click="onClickLoadDatabase"
        :disabled="listDatabases.length == 0 || !selectedDatabase"
        size="small"
      >
        Load
      </Button>
    </div>
    <Button
      :icon="isDarkMode ? 'pi pi-moon' : 'pi pi-sun'"
      @click="toggleDarkMode()"
      size="small"
    />
  </div>
  <div>
    <p v-if="loadedDatabase">Loaded Database: {{ this.loadedDatabase }}</p>
  </div>
  <div class="flex flex-wrap gap-2">
    <DataStructures
      v-if="loadedDatabase && dataStructures.length !== 0"
      :data="dataStructures"
      @loadDataStructure="onLoadDataStructure"
    />
    <ParameterFields
      v-if="loadedDatabase && parameterFields.length !== 0"
      :data="parameterFields"
      :sourceDataStructure="selectedDataStructure"
      @loadEnumValues="onLoadEnumValues"
    />
    <EnumDialog :data="enumValues" :name="selectedParameter" ref="enumDialog" />
  </div>
</template>

<script>
import DataStructures from './components/DataStructures.vue';
import ParameterFields from './components/ParameterFields.vue';
import EnumDialog from './components/EnumDialog.vue';

export default {
  name: 'App',
  components: { DataStructures, ParameterFields, EnumDialog },
  data() {
    return {
      dataStructures: [],
      parameterFields: [],
      enumValues: [],
      listDatabases: [],
      loadedDatabase: '',
      selectedDatabase: '',
      selectedDataStructure: '',
      selectedParameter: '',
      isDarkMode: document.documentElement.classList.contains('my-app-dark')
    };
  },
  mounted() {
    fetch('/api/v1/databases', {
      headers: {
        Accept: 'application/json'
      }
    })
      .then((res) => res.json())
      .then((data) => {
        this.listDatabases = data;
      });
  },
  methods: {
    // Toggle dark mode
    toggleDarkMode() {
      document.documentElement.classList.toggle('my-app-dark');
      this.isDarkMode =
        document.documentElement.classList.contains('my-app-dark');
    },
    // Load database from backend
    onClickLoadDatabase() {
      this.$refs.enumDialog.setVisible(false);
      this.dataStructures = [];
      this.parameterFields = [];
      this.loadedDatabase = '';
      fetch('/api/v1/databases', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ database: this.selectedDatabase })
      })
        .then((res) => {
          if (!res.ok) {
            return res.text().then((text) => {
              throw new Error(text);
            });
          }
          return res.json();
        })
        .then((data) => {
          this.loadedDatabase = this.selectedDatabase;
          this.dataStructures = data;
        })
        .catch((error) => {
          this.showError('Error Loading Database', error.message);
        });
    },
    // Load parameter fields for a specific data structure ID
    onLoadDataStructure(id, name) {
      this.$refs.enumDialog.setVisible(false);
      this.selectedDataStructure = name;
      fetch('/api/v1/datastructures', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ database: this.selectedDatabase, id: id })
      })
        .then((res) => {
          if (!res.ok) {
            return res.text().then((text) => {
              throw new Error(text);
            });
          }
          return res.json();
        })
        .then((data) => {
          this.parameterFields = data;
        })
        .catch((error) => {
          this.showError('Error Fetching Parameters', error.message);
        });
    },
    // Load enumeration values for a specific parameter ID
    onLoadEnumValues(id, name) {
      this.selectedParameter = name;
      fetch('/api/v1/enumerations', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ database: this.selectedDatabase, id: id })
      })
        .then((res) => {
          if (!res.ok) {
            return res.text().then((text) => {
              throw new Error(text);
            });
          }
          return res.json();
        })
        .then((data) => {
          this.enumValues = data;
          this.$refs.enumDialog.setVisible(true);
        })
        .catch((error) => {
          this.showError('Error Fetching Enumerations', error.message);
        });
    },
    // Show error toast
    showError(summary, detail) {
      this.$toast.add({
        severity: 'error',
        summary: summary,
        detail: detail,
        life: 3000
      });
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
