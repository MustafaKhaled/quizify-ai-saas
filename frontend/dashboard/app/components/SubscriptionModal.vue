<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const { startCheckout } = useSubscription()

const isLoading = ref(false)

const PRO_MONTHLY_PRICE_ID = 'price_1Slw1QGxfejNiimXsa3DfZ8R'
const PRO_YEARLY_PRICE_ID = 'price_1Slw1jGxfejNiimXMN0PHObK'

const selectedPlan = ref<'monthly' | 'yearly'>('monthly')

async function checkout() {
  isLoading.value = true
  const priceId = selectedPlan.value === 'yearly' ? PRO_YEARLY_PRICE_ID : PRO_MONTHLY_PRICE_ID
  await startCheckout(priceId)
  isLoading.value = false
}

function close() {
  emit('update:modelValue', false)
}
</script>

<template>
  <UModal :open="modelValue" @update:open="close">
    <template #content>
      <div class="p-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Upgrade to Pro</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
          Unlock unlimited quiz generation, all question types, and more.
        </p>

        <div class="grid grid-cols-2 gap-3 mb-6">
          <button
            class="p-4 rounded-lg border-2 text-left transition-colors"
            :class="selectedPlan === 'monthly'
              ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-200 dark:border-gray-700'"
            @click="selectedPlan = 'monthly'"
          >
            <p class="font-semibold text-gray-900 dark:text-white">Monthly</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">€7.99<span class="text-sm font-normal text-gray-500">/mo</span></p>
          </button>
          <button
            class="p-4 rounded-lg border-2 text-left transition-colors relative"
            :class="selectedPlan === 'yearly'
              ? 'border-blue-600 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-200 dark:border-gray-700'"
            @click="selectedPlan = 'yearly'"
          >
            <span class="absolute -top-2.5 right-2 bg-green-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">SAVE 25%</span>
            <p class="font-semibold text-gray-900 dark:text-white">Yearly</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">€5.99<span class="text-sm font-normal text-gray-500">/mo</span></p>
          </button>
        </div>

        <div class="flex gap-3">
          <UButton
            label="Subscribe"
            color="primary"
            block
            size="lg"
            :loading="isLoading"
            @click="checkout"
          />
          <UButton
            label="Cancel"
            color="neutral"
            variant="ghost"
            size="lg"
            @click="close"
          />
        </div>
      </div>
    </template>
  </UModal>
</template>
