import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  IconButton,
  Typography,
  Box,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import ContactForm from './ContactForm';

const ContactList = () => {
  const [contacts, setContacts] = useState([]);
  const [openForm, setOpenForm] = useState(false);
  const [editingContact, setEditingContact] = useState(null);
  const { user } = useAuth();

  const fetchContacts = async () => {
    try {
      const response = await axios.get('/api/contacts', {
        headers: { Authorization: `Bearer ${user.token}` },
      });
      setContacts(response.data);
    } catch (error) {
      console.error('Error fetching contacts:', error);
    }
  };

  useEffect(() => {
    fetchContacts();
  }, [user]);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/contacts/${id}`, {
        headers: { Authorization: `Bearer ${user.token}` },
      });
      fetchContacts();
    } catch (error) {
      console.error('Error deleting contact:', error);
    }
  };

  const handleEdit = (contact) => {
    setEditingContact(contact);
    setOpenForm(true);
  };

  const handleFormClose = () => {
    setOpenForm(false);
    setEditingContact(null);
  };

  const handleFormSubmit = () => {
    fetchContacts();
    handleFormClose();
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h4" component="h1">
            Address Book
          </Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => setOpenForm(true)}
          >
            Add Contact
          </Button>
        </Box>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Phone</TableCell>
                <TableCell>Address</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {contacts.map((contact) => (
                <TableRow key={contact.id}>
                  <TableCell>
                    {contact.first_name} {contact.last_name}
                  </TableCell>
                  <TableCell>{contact.email}</TableCell>
                  <TableCell>{contact.phone_number}</TableCell>
                  <TableCell>
                    {contact.street_address}
                    {contact.apartment_unit && `, ${contact.apartment_unit}`}
                    <br />
                    {contact.city}, {contact.zip_code}
                  </TableCell>
                  <TableCell>
                    <IconButton onClick={() => handleEdit(contact)} color="primary">
                      <EditIcon />
                    </IconButton>
                    <IconButton onClick={() => handleDelete(contact.id)} color="error">
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
      <ContactForm
        open={openForm}
        onClose={handleFormClose}
        onSubmit={handleFormSubmit}
        contact={editingContact}
      />
    </Container>
  );
};

export default ContactList; 