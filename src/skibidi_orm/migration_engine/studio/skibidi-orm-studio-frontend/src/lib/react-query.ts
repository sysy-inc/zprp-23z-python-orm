import {
    UseMutationOptions,
    UseQueryOptions
} from '@tanstack/react-query';

export type ReqQueryOptions<TQueryFn extends (...args: any) => any> = Pick<
    UseQueryOptions<Awaited<ReturnType<TQueryFn>>, Error>,
    'queryKey' | 'queryFn'
>
export type QueryConfig<TQueryFn extends (...args: any) => any, TData = Awaited<ReturnType<TQueryFn>>> = Omit<
    UseQueryOptions<Awaited<ReturnType<TQueryFn>>, Error, TData>,
    'queryKey' | 'queryFn'
>;
export type ApiFnReturnType<FnType extends (...args: any) => Promise<any>> =
    Awaited<ReturnType<FnType>>;

export type MutationConfig<
    MutationFnType extends (...args: any) => Promise<any>,
> = UseMutationOptions<
    ApiFnReturnType<MutationFnType>,
    Error,
    Parameters<MutationFnType>[0]
>;
