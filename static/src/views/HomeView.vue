<script setup>
  import { onMounted } from 'vue'
  import { RouterLink } from 'vue-router'
  import Header from '../components/Header.vue'
  import Footer from '../components/Footer.vue'
  import composable from '../composable'

  onMounted(() => composable.update_title('Home'))
</script>

<template>
  <Header />

  <main>
    <div>
      <section id = "banner">
        <h2 id = "banner-msg">Gerenciamento de Projetos Simplificado</h2>
        <p>Transforme sua organização com soluções eficientes.</p>
        <RouterLink to = '/projects'><button>Comece Agora</button></RouterLink>
      </section>

      <section id = "apresentation">
        <div class = "container">
          <h2>Aumente sua produtividade</h2>

          <div class = "content">
            <p>
              A organização é chave para o sucesso então não percas mais tempo,
              elimine ja toda a bagunça, gerencie todos os seus
              projetos de maneira facil e eficiente, controle o orçamento
              de cada um deles, os autores envolvidos a data do projeto etc.
            </p>

            <div>
              <div class = "loader">
                <div class = "loader-cube loader-cube-color"></div>
                <div class = "loader-cube loader-cube-glowing"></div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>

  <Footer />
</template>

<style scoped>
  main {
    margin-bottom: 40px;
    min-height: 100vh;
  }

  #banner {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    flex-direction: column;
    width: 100%;
    height: 100vh;
    background: var(--color-1);
    color: var(--color-3);
    animation: slideInDown 1s ease;
  }

  #banner h2 {
    font-size: 3rem;
    margin-bottom: 20px;
    opacity: 0;
    animation: fadeIn 2s ease forwards;
  }

  #banner p {
    font-size: 19.2px;
    margin-bottom: 30px;
  }

  #banner button {
    font-size: 16px;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
    border: none;
    background: var(--color-2);
    color: var(--color-3);
    transition: background-color 0.3s ease, transform 0.3s ease;
  }

  #banner button:hover {
      background-color: var(--color-4);
      transform: scale(1.1);
  }

  @keyframes slideInDown {
    from {
      transform: translateY(-100%);
    }

    to {
        transform: translateY(0);
    }
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }

    to {
      opacity: 1;
    }
  }

  #apresentation h2 {
    margin-bottom: 30px;
  }

  #apresentation p {
    max-width: 700px;
  }

  #apresentation .content {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding-right: 15px;
  }

  .loader {
    width: 150px;
    height: 150px;
    position: relative;
    align-items: center;
    justify-content: center;
  }

  .loader-cube {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 30px;
  }

  .loader-cube-glowing {
    z-index: 2;
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
  }

  .loader-cube-color {
    z-index: 1;
    background: linear-gradient(135deg, var(--color-2), var(--color-3));
    animation: loadtwo 2.5s ease-in-out infinite;
  }

  @keyframes loadtwo {
    50% {
      transform: rotate(-80deg);
    }
  }
</style>