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
  <DataStructures
    v-if="loadedDatabase && dataStructures.length !== 0"
    :data="dataStructures"
  />
</template>

<script>
import DataStructures from './components/DataStructures.vue';

export default {
  name: 'App',
  components: { DataStructures },
  data() {
    return {
      dataStructures: [],
      listDatabases: [],
      loadedDatabase: '',
      selectedDatabase: '',
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
      fetch('/api/v1/load', {
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
