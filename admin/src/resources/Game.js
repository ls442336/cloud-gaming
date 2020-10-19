import * as React from "react";
import { List, Datagrid, Edit, Create, SimpleForm, TextInput, ImageField, TextField, EditButton } from 'react-admin';
import pdfExporter from '../PdfExporter'
import moment from 'moment'

const gameExporter = (games) => {
    const fields = ['Id', 'Nome', 'Descrição', 'Bucket_id', 'Criado em']
    const data = games.map(game => [game.id, game.name, game.description, game.bucket_id, moment(game.createdAt).format('DD/MM/YYYY')])

    pdfExporter('relatórios_jogos.pdf', fields, data, 'Relatório de Jogos Cadastrados')
}

export const GameList = (props) => (
    <List {...props} exporter={gameExporter}>
        <Datagrid>
            {/* <TextField source="id" /> */}
            <ImageField source="thumbnail_url" label="Thumbnail" />
            <TextField source="name" label="Nome"/>
            <TextField source="description" label="Descrição"/>
            <TextField source="path"/>
            {/* <TextField source="bucket_id" /> */}
            {/* <ImageField source="background_url" label="Background" /> */}
            <EditButton basePath="/game" />
        </Datagrid>
    </List>
);

export const GameTitle = ({ record }) => {
    return <span>Jogo {record ? `"${record.name}"` : ''}</span>;
};

export const GameCreate = (props) => (
    <Create title="Adicionar Jogo" {...props}>
        <SimpleForm>
            <TextInput  source="name" label="Nome" fullWidth/>
            <TextInput  source="description" label="Descrição" multiline fullWidth/>
            <TextInput  source="path" label="Path" fullWidth />
            <TextInput  source="bucket_id" label="Bucket Id" fullWidth/>
            <TextInput  source="thumbnail_url" label="Thumbnail URL" fullWidth/>
            <TextInput  source="background_url" label="Background URL" fullWidth/>
        </SimpleForm>
    </Create>
);

export const GameEdit = (props) => (
    <Edit title={<GameTitle />} {...props}>
        <SimpleForm>
            <TextInput  source="name" label="Nome" fullWidth/>
            <TextInput  source="description" label="Descrição" multiline fullWidth/>
            <TextInput  source="path" label="Path" fullWidth/>
            <TextInput  source="bucket_id" label="Bucket Id" fullWidth/>
            <TextInput  source="thumbnail_url" label="Thumbnail URL" fullWidth/>
            <TextInput  source="background_url" label="Background URL" fullWidth />
        </SimpleForm>
    </Edit>
);