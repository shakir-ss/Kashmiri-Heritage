<template>
  <div class="about-view">
    <!-- Hero Section -->
    <section class="about-hero">
      <div class="container hero-content">
        <h1>Our Kashmiri <span>Legacy</span></h1>
        <p>Preserving centuries of artisanal excellence, one masterpiece at a time.</p>
      </div>
    </section>

    <!-- Our Story -->
    <section class="story-section container">
      <div class="story-grid">
        <div class="story-text">
          <span class="category-tag">Established 1984</span>
          <h2>The Soul of the Valley</h2>
          <p>The Hundred Villages was born from a simple yet profound desire: to bridge the gap between the secluded artisans of the Himalayas and the global connoisseurs of fine craft. For generations, our family has worked alongside the master weavers, wood-carvers, and farmers of the Kashmir Valley.</p>
          <p>We don't just sell products; we curate stories. Every Pashmina, every Papier Mâché box, and every gram of Saffron we offer is a testament to a heritage that has survived empires and outlasted industrialization.</p>
        </div>
        <div class="story-image card artisan-border">
          <img src="https://images.unsplash.com/photo-1566908829550-e6551b00979b?auto=format&fit=crop&q=80&w=800" alt="Kashmiri Landscape" />
        </div>
      </div>
    </section>

    <!-- Our Values -->
    <section class="values-section kashmiri-pattern">
      <div class="container">
        <div class="section-header">
          <h2>The Pillars of Heritage</h2>
        </div>
        <div class="values-grid">
          <div class="value-card card">
            <div class="value-icon">🤝</div>
            <h3>Direct Sourcing</h3>
            <p>We eliminate middlemen to ensure that the maximum value of every purchase goes directly to the artisan's pocket.</p>
          </div>
          <div class="value-card card">
            <div class="value-icon">🏆</div>
            <h3>Unyielding Quality</h3>
            <p>From lab-certified Mongra Saffron to hand-spun Pashmina, we never compromise on the authenticity of our offerings.</p>
          </div>
          <div class="value-card card">
            <div class="value-icon">🌿</div>
            <h3>Organic Roots</h3>
            <p>Our dry fruits are grown in the high-altitude orchards of Kashmir, using traditional, chemical-free farming methods.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Cultural Impact -->
    <section class="impact-section container">
      <div class="impact-content">
        <h2>Sustaining a Way of Life</h2>
        <p>By bringing Kashmiri treasures to the world, we are helping sustain a community of over 500 local artisans and farmers. Your support ensures that the ancient techniques of Sozni embroidery, Walnut wood carving, and Kani weaving are passed down to the next generation.</p>
        <div class="impact-stats">
          <div class="stat">
            <span class="number">500+</span>
            <span class="label">Artisans Supported</span>
          </div>
          <div class="stat">
            <span class="number">100%</span>
            <span class="label">Authentic Sourcing</span>
          </div>
          <div class="stat">
            <span class="number">20+</span>
            <span class="label">Global Destinations</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-hero {
  height: 60vh;
  /* background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://images.unsplash.com/photo-1598305371124-42ce18a75201?auto=format&fit=crop&q=80&w=1200"); */
  background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://drive.google.com/file/d/1oNpP9gmSEP7VARd0ZWefhyGzZ1Lf5D-Q/view");
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  color: white;
  text-align: center;
}

.hero-content {
  max-width: 800px;
}

.about-hero h1 { font-size: 4rem; margin-bottom: 1rem; }
.about-hero h1 span { color: var(--secondary); }
.about-hero p { font-size: 1.5rem; opacity: 0.9; font-weight: 300; }

.story-section { padding: 8rem 0; }
.story-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 5rem; align-items: center; }
.story-text h2 { font-size: 2.5rem; color: var(--primary); margin: 1.5rem 0; }
.story-text p { margin-bottom: 1.5rem; color: #555; }

.story-image img { width: 100%; border-radius: 15px; display: block; }

.values-section { padding: 8rem 0; background-color: #f9f6f2; }
.values-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.5rem; }
.value-card { padding: 3rem 2rem; text-align: center; }
.value-icon { font-size: 3rem; margin-bottom: 1.5rem; }
.value-card h3 { color: var(--primary); margin-bottom: 1rem; }

.impact-section { padding: 8rem 0; text-align: center; }
.impact-content { max-width: 900px; margin: 0 auto; }
.impact-content h2 { font-size: 2.5rem; color: var(--primary); margin-bottom: 2rem; }
.impact-content p { font-size: 1.2rem; color: #666; margin-bottom: 4rem; }

.impact-stats { display: flex; justify-content: center; gap: 5rem; }
.stat .number { display: block; font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; color: var(--secondary); }
.stat .label { font-size: 0.9rem; text-transform: uppercase; color: #888; letter-spacing: 1px; }

@media (max-width: 768px) {
  .story-grid { grid-template-columns: 1fr; gap: 3rem; }
  .values-grid { grid-template-columns: 1fr; }
  .impact-stats { flex-direction: column; gap: 3rem; }
}
</style>
