import {ISlashCommand, SlashCommandContext} from '@rocket.chat/apps-engine/definition/slashcommands';
import {IModify, IRead} from '@rocket.chat/apps-engine/definition/accessors';
import {App} from '@rocket.chat/apps-engine/definition/App';

export class HandoffCommand implements ISlashCommand {
    public command = 'handoff';
    public i18nDescription = 'Transfers to human agent';
    public i18nParamsExample = '';
    public providesPreview = false;

    constructor(private readonly app: App) {}

    public async executor(context: SlashCommandContext, read: IRead, modify: IModify): Promise<void> {
        const message = 'talk to support team';

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