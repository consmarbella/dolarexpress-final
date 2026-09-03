export default async function handler(req, res) {
  const { status } = req.query;

  if (status === 'success') {
    res.redirect(302, '/billing?status=success');
  } else {
    res.redirect(302, '/billing?status=cancel');
  }
}
