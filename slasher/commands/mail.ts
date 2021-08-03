import {ISlashCommand, SlashCommandContext} from '@rocket.chat/apps-engine/definition/slashcommands';
import {IModify, IRead} from '@rocket.chat/apps-engine/definition/accessors';
import {App} from '@rocket.chat/apps-engine/definition/App';

export class MailCommand implements ISlashCommand {
    public command = 'mail';
    public i18nDescription = 'Sends a mail';
    public i18nParamsExample = '';
    public providesPreview = false;

    constructor(private readonly app: App) {}

    public async executor(context: SlashCommandContext, read: IRead, modify: IModify): Promise<void> {
        const message = 'mail';

        const messageStructure = await modify.getCreator().startMessage();
        const sender = context.getSender(); // the user calling the slashcommand
        const room = context.getRoom(); // the current room

        messageStructure
        .setSender(sender)
        .setRoom(room)
        .setText(message);

        await modify.getCreator().finish(messageStructure);
    }
}