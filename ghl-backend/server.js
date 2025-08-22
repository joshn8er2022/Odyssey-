const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true
}));
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    service: 'GoHighLevel Backend API'
  });
});

// Helper function to get access token
async function getAccessToken() {
  try {
    const response = await axios.post(
      'https://services.leadconnectorhq.com/oauth/token',
      new URLSearchParams({
        client_id: process.env.GHL_API_KEY,
        client_secret: process.env.GHL_PRIVATE_KEY,
        grant_type: 'client_credentials'
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }
      }
    );
    return response.data.access_token;
  } catch (error) {
    console.error('Error getting access token:', error.response?.data || error.message);
    throw new Error('Failed to authenticate with GoHighLevel');
  }
}

// Classify lead with AI analysis
function classifyLead(contact) {
  const tags = contact.tags || [];
  const name = (contact.firstName + ' ' + contact.lastName).toLowerCase();
  const email = (contact.email || '').toLowerCase();
  
  // High-value indicators
  if (tags.some(tag => ['vip', 'enterprise', 'priority', 'hot'].includes(tag.toLowerCase())) ||
      email.includes('ceo') || email.includes('founder') || email.includes('director')) {
    return 'hot';
  }
  
  // Engaged indicators
  if (contact.lastMessageDate || 
      tags.some(tag => ['interested', 'demo', 'trial'].includes(tag.toLowerCase()))) {
    return 'warm';
  }
  
  // Default
  return 'cold';
}

// Main sync endpoint
app.post('/api/ghl/sync', async (req, res) => {
  try {
    const token = await getAccessToken();
    const locationId = process.env.GHL_LOCATION_ID;
    
    // Fetch all data in parallel
    const [contactsRes, opportunitiesRes, appointmentsRes, formsRes] = await Promise.all([
      axios.get(`https://services.leadconnectorhq.com/contacts/?locationId=${locationId}`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Version': '2021-07-28'
        }
      }),
      axios.get(`https://services.leadconnectorhq.com/opportunities/search?location_id=${locationId}`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Version': '2021-07-28'
        }
      }),
      axios.get(`https://services.leadconnectorhq.com/appointments/?locationId=${locationId}`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Version': '2021-07-28'
        }
      }),
      axios.get(`https://services.leadconnectorhq.com/forms/?locationId=${locationId}`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Version': '2021-07-28'
        }
      })
    ]);

    // Process contacts into leads
    const leads = contactsRes.data.contacts.map(contact => ({
      id: contact.id,
      name: `${contact.firstName || ''} ${contact.lastName || ''}`.trim(),
      email: contact.email,
      phone: contact.phone,
      status: classifyLead(contact),
      source: contact.source || 'GoHighLevel',
      lastContact: contact.dateUpdated,
      tags: contact.tags || [],
      customFields: contact.customFields || {},
      // Link opportunities
      opportunities: opportunitiesRes.data.opportunities
        .filter(opp => opp.contact.id === contact.id)
        .map(opp => ({
          id: opp.id,
          name: opp.name,
          status: opp.status,
          value: opp.monetaryValue,
          stage: opp.pipelineStageId
        })),
      // Link appointments
      appointments: appointmentsRes.data.appointments
        .filter(apt => apt.contactId === contact.id)
        .map(apt => ({
          id: apt.id,
          title: apt.title,
          startTime: apt.startTime,
          status: apt.status
        }))
    }));

    // Build summary
    const summary = {
      totalLeads: leads.length,
      leadsByStatus: {
        hot: leads.filter(l => l.status === 'hot').length,
        warm: leads.filter(l => l.status === 'warm').length,
        cold: leads.filter(l => l.status === 'cold').length
      },
      totalOpportunities: opportunitiesRes.data.opportunities.length,
      totalAppointments: appointmentsRes.data.appointments.length,
      forms: formsRes.data.forms.map(form => ({
        id: form.id,
        name: form.name,
        submissions: form.submissions || 0
      }))
    };

    res.json({
      success: true,
      timestamp: new Date().toISOString(),
      data: {
        leads,
        summary,
        raw: {
          contactsCount: contactsRes.data.contacts.length,
          opportunitiesCount: opportunitiesRes.data.opportunities.length,
          appointmentsCount: appointmentsRes.data.appointments.length,
          formsCount: formsRes.data.forms.length
        }
      }
    });

  } catch (error) {
    console.error('Sync error:', error.response?.data || error.message);
    res.status(500).json({
      success: false,
      error: error.message,
      details: error.response?.data
    });
  }
});

// Get forms endpoint
app.get('/api/ghl/forms', async (req, res) => {
  try {
    const token = await getAccessToken();
    const locationId = process.env.GHL_LOCATION_ID;
    
    const response = await axios.get(
      `https://services.leadconnectorhq.com/forms/?locationId=${locationId}`,
      {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Version': '2021-07-28'
        }
      }
    );

    res.json({
      success: true,
      forms: response.data.forms
    });

  } catch (error) {
    console.error('Forms error:', error.response?.data || error.message);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Webhook endpoint for real-time updates
app.post('/api/ghl/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  try {
    const event = JSON.parse(req.body.toString());
    console.log('Webhook received:', event.type, event.data?.id);
    
    // Process different event types
    switch(event.type) {
      case 'contact.create':
      case 'contact.update':
        // Handle contact events
        break;
      case 'opportunity.create':
      case 'opportunity.update':
        // Handle opportunity events
        break;
      case 'appointment.create':
      case 'appointment.update':
        // Handle appointment events
        break;
    }
    
    res.json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(400).json({ error: 'Invalid webhook data' });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: err.message
  });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`GoHighLevel backend running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});

module.exports = app;