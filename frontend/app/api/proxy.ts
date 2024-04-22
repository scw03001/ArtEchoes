// pages/api/proxy.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { id } = req.query;  // Extracting 'id' from the query parameter

  try {
    const url = `http://localhost:5000/find_artist/${id}`;
    const backendResponse = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!backendResponse.ok) {
      throw new Error(`Failed to fetch. Status: ${backendResponse.status}`);
    }

    const data = await backendResponse.json();
    res.status(200).json(data);
  } catch (error) {
    console.error("Proxy error:", error);
    // res.status(500).json({ message: error.message });
  }
}
