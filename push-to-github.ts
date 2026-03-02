import git from 'isomorphic-git';
import http from 'isomorphic-git/http/node';
import fs from 'fs';
import path from 'path';

async function pushToGitHub() {
  const dir = process.cwd();
  const token = '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';
  const repoUrl = 'https://github.com/consmarbella/dolarexpress-final.git';

  try {
    console.log('Sincronizando cambios finales con GitHub (Fix class vs className)...');

    if (!fs.existsSync(path.join(dir, '.git'))) {
      await git.init({ fs, dir });
    }

    try {
      await git.addRemote({ fs, dir, remote: 'origin', url: repoUrl });
    } catch (e) {}

    await git.setConfig({ fs, dir, path: 'user.name', value: 'DolarExpress Bot' });
    await git.setConfig({ fs, dir, path: 'user.email', value: 'bot@dolarexpress.cl' });

    const files = await fs.promises.readdir(dir);
    for (const file of files) {
      if (['node_modules', '.git', 'dist', '.next'].includes(file)) continue;
      await git.add({ fs, dir, filepath: file });
    }

    const sha = await git.commit({
      fs,
      dir,
      message: 'Fix: className instead of class in Home.tsx and add lint script',
      author: { name: 'DolarExpress Bot', email: 'bot@dolarexpress.cl' }
    });
    console.log(`Commit: ${sha}`);

    try {
      await git.branch({ fs, dir, ref: 'main', checkout: true });
    } catch (e) {}

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
      console.log('¡Sincronización completada con éxito!');
    } else {
      console.error('Error en el push:', pushResult);
    }
  } catch (error) {
    console.error('Error durante el proceso:', error);
    process.exit(1);
  }
}

pushToGitHub();
