<template>
  <div class="flex">
    <DataTable
      v-model:filters="filters"
      :value="data"
      paginator
      :rows="10"
      dataKey="id"
      filterDisplay="row"
      :globalFilterFields="['name', 'channel', 'source']"
      size="small"
    >
      <template #header>
        <div class="flex justify-end">
          <IconField>
            <InputIcon>
              <i class="pi pi-search" />
            </InputIcon>
            <InputText
              v-model="filters['global'].value"
              placeholder="Keyword Search"
              size="small"
            />
          </IconField>
        </div>
      </template>
      <template #empty> No data structures found. </template>
      <Column field="name" header="Engineering Name" style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.name }}
        </template>
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            type="text"
            @input="filterCallback()"
            placeholder="Search by name"
            size="small"
          />
        </template>
      </Column>
      <Column field="channel" header="Channel" style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.channel }}
        </template>
        <template #filter="{ filterModel, filterCallback }">
          <InputText
            v-model="filterModel.value"
            type="number"
            @input="filterCallback()"
            placeholder="Search by channel"
            size="small"
          />
        </template>
      </Column>
      <Column field="source" header="Source Partition" style="min-width: 12rem">
        <template #body="{ data }">
          {{ data.source }}
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import { FilterMatchMode } from '@primevue/core/api';

export default {
  name: 'DataStructures',
  props: {
    data: []
  },
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
        channel: { value: null, matchMode: FilterMatchMode.EQUALS }
      }
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
