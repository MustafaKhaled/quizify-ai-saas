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
        <h2 class="text-xl font-bold gradient-text mb-2">Upgrade to Pro</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mb-6">
          Unlock unlimited quiz generation, all question types, and more.
        </p>

        <div class="grid grid-cols-2 gap-3 mb-6">
          <button
            type="button"
            class="p-4 rounded-xl text-left transition-all glass-card"
            :class="selectedPlan === 'monthly'
              ? 'ring-2 ring-blue-500 bg-blue-500/15 shadow-lg shadow-blue-500/20 scale-[1.02]'
              : 'ring-1 ring-transparent hover:ring-blue-500/30'"
            @click="selectedPlan = 'monthly'"
          >
            <div class="flex items-center justify-between mb-1">
              <p class="font-semibold text-slate-900 dark:text-white">Monthly</p>
              <UIcon
                v-if="selectedPlan === 'monthly'"
                name="i-lucide-check-circle-2"
                class="w-5 h-5 text-blue-500"
              />
            </div>
            <p class="text-2xl font-bold gradient-text mt-1">€7.99<span class="text-sm font-normal text-slate-500">/mo</span></p>
          </button>
          <button
            type="button"
            class="p-4 rounded-xl text-left transition-all glass-card relative"
            :class="selectedPlan === 'yearly'
              ? 'ring-2 ring-blue-500 bg-blue-500/15 shadow-lg shadow-blue-500/20 scale-[1.02]'
              : 'ring-1 ring-transparent hover:ring-blue-500/30'"
            @click="selectedPlan = 'yearly'"
          >
            <span class="absolute -top-2.5 right-2 bg-gradient-to-r from-green-500 to-teal-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">SAVE 25%</span>
            <div class="flex items-center justify-between mb-1">
              <p class="font-semibold text-slate-900 dark:text-white">Yearly</p>
              <UIcon
                v-if="selectedPlan === 'yearly'"
                name="i-lucide-check-circle-2"
                class="w-5 h-5 text-blue-500"
              />
            </div>
            <p class="text-2xl font-bold gradient-text mt-1">€5.99<span class="text-sm font-normal text-slate-500">/mo</span></p>
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
