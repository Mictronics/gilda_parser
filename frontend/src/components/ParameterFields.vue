<template>
  <div class="flex">
    <DataTable
      v-model:filters="filters"
      :value="data"
      paginator
      :rows="10"
      dataKey="id"
      filterDisplay="row"
      :globalFilterFields="['name', 'description', 'comment']"
      size="small"
    >
      <template #header>
        <div class="flex justify-content-between">
          <div class="text-xl pr-2">{{ sourceDataStructure }}</div>
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
      <template #empty> No parameter fields found. </template>
      <Column field="name" header="Engineering Name" style="min-width: 12rem">
        <template #body="{ data }">
          <div>
            <div class="grid">
              <div class="col">
                <Button
                  :label="data.name"
                  variant="link"
                  @click="onParameterClick(data.id, data.name, $event)"
                  style="padding-left: 0"
                  v-if="linkTypes.includes(data.type)"
                />
                <div class="no-button" v-else>{{ data.name }}</div>
                <div v-if="data.reference" class="text-xs font-light">
                  {{ data.reference }}
                </div>
                <div v-if="data.desc" class="text-xs font-light">
                  {{ data.desc }}
                </div>
                <div v-if="data.comment" class="text-xs font-light">
                  {{ data.comment }}
                </div>
              </div>
              <div class="col">
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
                      <td>Low Bit:</td>
                      <td>{{ data.lowBit }}</td>
                      <td class="pl-2">High Bit:</td>
                      <td>{{ data.hiBit }}</td>
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
  name: 'ParameterFields',
  props: {
    data: Array,
    sourceDataStructure: String
  },
  emits: ['loadEnumValues'],
  data() {
    return {
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        name: { value: null, matchMode: FilterMatchMode.STARTS_WITH }
      },
      linkTypes: ['enum', 'fifo', 'struct', 'A429']
    };
  },
  methods: {
    onParameterClick(id, name, ev) {
      this.$emit('loadEnumValues', id, name);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.no-button {
  padding: var(--p-button-padding-y) 0rem 1rem;
}
</style>
