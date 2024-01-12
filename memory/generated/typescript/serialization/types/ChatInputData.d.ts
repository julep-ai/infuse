/**
 * This file was auto-generated by Fern from our API Definition.
 */
import * as serializers from "..";
import * as JulepApi from "../../api";
import * as core from "../../core";
export declare const ChatInputData: core.serialization.ObjectSchema<serializers.ChatInputData.Raw, JulepApi.ChatInputData>;
export declare namespace ChatInputData {
    interface Raw {
        messages: serializers.InputChatMlMessage.Raw[];
        tools?: serializers.Tool.Raw[] | null;
        tool_choice?: serializers.ToolChoiceOption.Raw | null;
    }
}
