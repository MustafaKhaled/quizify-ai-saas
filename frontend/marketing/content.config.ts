import { defineCollection, z } from '@nuxt/content'

const variantEnum = z.enum(['solid', 'outline', 'subtle', 'soft', 'ghost', 'link'])
const colorEnum = z.enum(['primary', 'secondary', 'neutral', 'error', 'warning', 'success', 'info'])
const sizeEnum = z.enum(['xs', 'sm', 'md', 'lg', 'xl'])
const orientationEnum = z.enum(['vertical', 'horizontal'])

const createBaseSchema = () => z.object({
  title: z.string().nonempty(),
  description: z.string().nonempty()
})

const createFeatureItemSchema = () => createBaseSchema().extend({
  icon: z.string().nonempty().editor({ input: 'icon' })
})

const createLinkSchema = () => z.object({
  label: z.string().nonempty(),
  to: z.string().nonempty(),
  icon: z.string().optional().editor({ input: 'icon' }),
  size: sizeEnum.optional(),
  trailing: z.boolean().optional(),
  target: z.string().optional(),
  color: colorEnum.optional(),
  variant: variantEnum.optional()
})

const createImageSchema = () => z.object({
  src: z.string().nonempty().editor({ input: 'media' }),
  alt: z.string().optional(),
  loading: z.enum(['lazy', 'eager']).optional(),
  srcset: z.string().optional()
})

export const collections = {
  index: defineCollection({
    source: '0.index.yml',
    type: 'page',
    schema: z.object({
      hero: z.object(({
        links: z.array(createLinkSchema())
      })),
      sections: z.array(
        createBaseSchema().extend({
          id: z.string().nonempty(),
          orientation: orientationEnum.optional(),
          reverse: z.boolean().optional(),
          // image + caption are optional — sections that render a custom slot
          // (e.g. SubjectShowcase) don't need them.
          image: z.string().optional(),
          imageCaption: z.string().optional(),
          // features are optional — the SubjectShowcase section omits them.
          features: z.array(createFeatureItemSchema()).optional()
        })
      ),
      features: createBaseSchema().extend({
        items: z.array(createFeatureItemSchema())
      }),
      testimonials: createBaseSchema().extend({
        headline: z.string().optional(),
        items: z.array(
          z.object({
            quote: z.string().nonempty(),
            user: z.object({
              name: z.string().nonempty(),
              description: z.string().nonempty(),
              to: z.string().nonempty(),
              target: z.string().nonempty(),
              avatar: createImageSchema()
            })
          })
        )
      }),
      cta: createBaseSchema().extend({
        links: z.array(createLinkSchema())
      })
    })
  }),
  docs: defineCollection({
    source: '1.docs/**/*',
    type: 'page'
  }),
  pricing: defineCollection({
    source: '2.pricing.yml',
    type: 'page',
    schema: z.object({
      plans: z.array(
        z.object({
          title: z.string().nonempty(),
          description: z.string().nonempty(),
          price: z.object({
            month: z.string().nonempty(),
            year: z.string().nonempty()
          }),
          billing_period: z.string().nonempty(),
          billing_cycle: z.string().nonempty(),
          button: createLinkSchema(),
          features: z.array(z.string().nonempty()),
          highlight: z.boolean().optional()
        })
      ),
      logos: z.object({
        title: z.string().nonempty(),
        icons: z.array(z.string())
      }),
      faq: createBaseSchema().extend({
        items: z.array(
          z.object({
            label: z.string().nonempty(),
            content: z.string().nonempty()
          })
        )
      })
    })
  }),
  blog: defineCollection({
    source: '3.blog.yml',
    type: 'page'
  }),
  posts: defineCollection({
    source: '3.blog/**/*',
    type: 'page',
    schema: z.object({
      image: z.object({ src: z.string().nonempty().editor({ input: 'media' }) }),
      authors: z.array(
        z.object({
          name: z.string().nonempty(),
          to: z.string().nonempty(),
          avatar: z.object({ src: z.string().nonempty().editor({ input: 'media' }) })
        })
      ),
      date: z.date(),
      badge: z.object({ label: z.string().nonempty() })
    })
  }),
  changelog: defineCollection({
    source: '4.changelog.yml',
    type: 'page'
  }),
  versions: defineCollection({
    source: '4.changelog/**/*',
    type: 'page',
    schema: z.object({
      title: z.string().nonempty(),
      description: z.string(),
      date: z.date(),
      image: z.string()
    })
  }),
  faq: defineCollection({
    source: '5.faq.yml', // This matches the filename you mentioned
    type: 'page',
    schema: z.object({
      title: z.string().nonempty(),
      description: z.string().nonempty(),
      items: z.array(
        z.object({
          label: z.string().nonempty(),
          content: z.string().nonempty()
        })
      )
    })
  }),
  exams: defineCollection({
    // Niche exam-specific landing pages. One YAML per exam under content/6.exams/.
    // Each renders at /exams/<filename> via app/pages/exams/[slug].vue.
    source: '6.exams/**/*',
    type: 'page',
    schema: z.object({
      subject_slug: z.string().nonempty(),
      color: z.string().nonempty(),
      icon: z.string().nonempty(),
      badge: z.string().nonempty(),
      exam_authority: z.string().optional(),
      hero: z.object({
        headline: z.string().nonempty(),
        subhead: z.string().nonempty(),
        tagline: z.string().optional(),
        cta: createLinkSchema()
      }),
      pains: createBaseSchema().extend({
        items: z.array(z.string().nonempty())
      }),
      promises: createBaseSchema().extend({
        items: z.array(createFeatureItemSchema())
      }),
      comparison: createBaseSchema().extend({
        columns: z.array(z.object({
          name: z.string().nonempty(),
          highlight: z.boolean().optional()
        })),
        rows: z.array(z.object({
          feature: z.string().nonempty(),
          // One status per column, in the same order. Allowed: 'yes', 'no', 'partial'.
          values: z.array(z.enum(['yes', 'no', 'partial']))
        }))
      }),
      faq: z.object({
        title: z.string().optional(),
        items: z.array(z.object({
          label: z.string().nonempty(),
          content: z.string().nonempty()
        }))
      }),
      testimonials: z.object({
        title: z.string().optional(),
        items: z.array(z.object({
          quote: z.string().nonempty(),
          user: z.object({
            name: z.string().nonempty(),
            description: z.string().nonempty(),
            avatar: createImageSchema().optional()
          })
        }))
      }).optional()
    })
  })
}
