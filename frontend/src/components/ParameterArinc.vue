<template>
  <div class="flex">
    <DataTable
      v-model:filters="filters"
      :value="data"
      paginator
      :rows="10"
      dataKey="id"
      filterDisplay="row"
      :globalFilterFields="['name', 'description']"
      size="small"
    >
      <template #header>
        <div class="flex justify-content-between">
          <div class="text-xl pr-2">{{ sourceParameterField }}</div>
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
      <template #empty> No ARINC parameters found. </template>
      <Column field="name" header="Name" style="min-width: 12rem">
        <template #body="{ data }">
          <div>
            <div class="grid">
              <div class="col">
                <div class="no-button">{{ data.name }}</div>
                <div v-if="data.fifo" class="text-xs font-light">
                  {{ data.fifo }}
                </div>
                <div v-if="data.desc" class="text-xs font-light">
                  {{ data.desc }}
                </div>
              </div>
              <div class="col col-align-end">
                <table class="text-xs font-light">
                  <tbody>
                    <tr>
                      <td>Offset:</td>
                      <td>{{ data.offset }}</td>
                      <td class="pl-2">Size:</td>
                      <td>{{ data.size }}</td>
                    </tr>
                    <tr>
                      <td>Type:</td>
                      <td>{{ data.type }}</td>
                      <td class="pl-2">Unit:</td>
                      <td v-if="data.unit != 'unitless'">{{ data.unit }}</td>
                    </tr>
                    <tr>
                      <td>Min:</td>
                      <td>{{ data.min }}</td>
                      <td class="pl-2">Max:</td>
                      <td>{{ data.max }}</td>
                    </tr>
                    <tr>
                      <td>Scale:</td>
                      <td>{{ data.scale }}</td>
                      <td class="pl-2">Label:</td>
                      <td>{{ data.label }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
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
    </DataTable>
  </div>
</template>

<script>
import { FilterMatchMode } from '@primevue/core/api';

export default {
  name: 'ParameterArinc',
  props: {
    data: Array,
    sourceParameterField: String
  },
  emits: [],
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
      }
    };
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.no-button {
  padding: var(--p-button-padding-y) 0rem 1rem;
}
.col-align-end {
  text-align: -webkit-right;
}
</style>
