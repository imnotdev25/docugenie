const apiMiddleware = (req, res, next) => {
  const apiUrl = process.env.API_URL;
  if (req.url.startsWith('/api/')) {
    req.url = `${apiUrl}${req.url.replace('/api', '')}`;
  }
  next();
};

export default apiMiddleware;