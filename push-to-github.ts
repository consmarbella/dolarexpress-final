import git from 'isomorphic-git';
import http from 'isomorphic-git/http/node';
import fs from 'fs';
import path from 'path';

async function pushToGitHub() {
  const dir = process.cwd();
  const token = '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';
  const repoUrl = 'https://github.com/consmarbella/dolarexpress-final.git';

  try {
    console.log('Iniciando proceso de push a GitHub...');

    // Inicializar repo si no existe
    if (!fs.existsSync(path.join(dir, '.git'))) {
      await git.init({ fs, dir });
    }

    // Añadir remoto origin si no existe
    try {
      await git.addRemote({
        fs,
        dir,
        remote: 'origin',
        url: repoUrl
      });
    } catch (e) {
      // Ya existe o error al añadir
    }

    // Configurar usuario (necesario para commit)
    await git.setConfig({
      fs,
      dir,
      path: 'user.name',
      value: 'DolarExpress Bot'
    });
    await git.setConfig({
      fs,
      dir,
      path: 'user.email',
      value: 'bot@dolarexpress.cl'
    });

    // Añadir todos los archivos (excepto los ignorados)
    const files = await fs.promises.readdir(dir);
    for (const file of files) {
      if (file === 'node_modules' || file === '.git' || file === 'dist' || file === '.next') continue;
      await git.add({ fs, dir, filepath: file });
    }

    // Crear commit
    const sha = await git.commit({
      fs,
      dir,
      message: 'Actualización automática: pSEO, SEO dinámico y correcciones de rutas',
      author: {
        name: 'DolarExpress Bot',
        email: 'bot@dolarexpress.cl'
      }
    });
    console.log(`Commit creado: ${sha}`);

    // Asegurar que estamos en la rama main
    try {
      await git.branch({
        fs,
        dir,
        ref: 'main',
        checkout: true
      });
    } catch (e) {
      // Si ya existe o hay error, intentamos continuar
    }

    // Push
    const pushResult = await git.push({
      fs,
      http,
      dir,
      remote: 'origin',
      ref: 'main',
      force: true,
      onAuth: () => ({ username: token, password: '' }),
    });

    if (pushResult.ok) {
      console.log('¡Push completado con éxito!');
    } else {
      console.error('Error en el push:', pushResult);
    }
  } catch (error) {
    console.error('Error durante el proceso:', error);
    process.exit(1);
  }
}

pushToGitHub();
